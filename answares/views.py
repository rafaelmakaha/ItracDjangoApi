# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import requests
from django.shortcuts import render
from rest_framework import viewsets

from answares.auth_data import username, password, servicos_username, servicos_password
from .models import Answares, Horario, Orgao, Servico
from .serializers import AnswaresSerializer, ServicoSerializer, OrgaoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .customLibs.connect_database import ConnectDatabase
from .customLibs.servicos_orgaos import ServicosOrgaos
import time


class AnswaresViewSet(viewsets.ModelViewSet):
    queryset = Answares.objects.all()
    serializer_class = AnswaresSerializer

    def update(self, request, *args, **kwargs):
        # alterar: lime_id, servico_id, servico_nome, status
        instance = self.get_object()
        servicos = ServicosOrgaos.returnServicos()
        if not self.request.data['servico_nome'] in servicos:
            # fazer post para nova ID de serviço
            response = ServicosOrgaos.create_servico(self.request.data,servicos_username,servicos_password)
            
            pass
        else:
            try:
                survey_id = self.request.data['survey_id']
                answare_id = self.request.data['answare_id']
                answare_id = ''.join(answare_id.split(survey_id))
                servico_id = self.request.data['servico_id']
                ConnectDatabase.updateQueryAnsware(survey_id=survey_id, answare_id=answare_id, servico_id=servico_id)
            except:
                return Response({"status": "Failure"})
        super(AnswaresViewSet, self).update(request, *args, **kwargs)
        return Response({"status": "Success"})

class PendingsList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        # atual = time.time()
        # print(atual) '1158'
        # if horario_atual - horario_banco > 1h:
        orgaos = ServicosOrgaos.returnOrgaosObjects()
        for orgao in orgaos:
            try:
                Orgao.objects.create(
                    id=orgao['orgao_id'],
                    nome=orgao['orgao_nome']
                )
            except:
                pass
            for servico in orgao['servicos']:
                try:
                    parent = Orgao.objects.get(id=orgao['orgao_id'])
                    Servico.objects.create(
                        id=servico['servico_id'],
                        nome=servico['servico_nome'],
                        orgao=parent
                    )
                except:
                    pass


        survey = '311832'
        newAnswares = ServicosOrgaos.getLimesureveyAnswers(survey, username, password)
        servicos_orgaos = ServicosOrgaos.returnOrgaos()
        for answare in newAnswares:
            try:
                id_orgao = answare['A qual instituição você pertence?'].split('-')[1].strip()
                id_orgao = id_orgao.zfill(8)
                if answare['Informe o nome do serviço que será avaliado nessa pesquisa.'] == 'Outros':
                    nome_servico = answare['Informe o nome do serviço que será avaliado nessa pesquisa. [Outros]']
                    id_servico = '0000'
                    answare_id = survey + str(answare['ID da resposta'])
                else:
                    continue
                orgao_nome = servicos_orgaos[str(int(id_orgao))][0]['orgao_nome']
                survey_id = survey
                lime_id = id_orgao + id_servico
                Answares.objects.create(
                    answare_id=answare_id,
                    lime_id=lime_id,
                    survey_id=survey_id,
                    servico_id=id_servico,
                    orgao_id=id_orgao,
                    orgao_nome=orgao_nome,
                    servico_nome=nome_servico,
                    status="N"
                )
            except:
                print('Valores incompatíveis')
                continue
        pendings = Answares.objects.filter(status='N')
        serializer = AnswaresSerializer(pendings, many=True, context={'request': request})
        return Response(serializer.data)


class ProcessedsList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        processeds = Answares.objects.filter(status='P')
        serializer = AnswaresSerializer(processeds, many=True, context={'request': request})
        return Response(serializer.data)


class OrgaoViewSet(viewsets.ModelViewSet):
    queryset = Orgao.objects.all()
    serializer_class = OrgaoSerializer


class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

# class ServicosList(viewsets.ViewSet):
#     serializer_class = ServicoSerializer
#     def get(self, request, format=None):
#         servicos = ServicosOrgaos.returnServicosObjects()
#         serializer = ServicoSerializer(servicos, many=True, context={'request': request})
#         return Response(serializer.data)

# class OrgaosList(viewsets.ViewSet):
#     serializer_class = OrgaoSerializer
#     def get(self, request, format=None):
#         orgaos = ServicosOrgaos.returnOrgaosObjects()
#         serializer = OrgaoSerializer(orgaos, many=True, context={'request': request})
#         return Response(serializer.data)
