# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .models import Answares, Horario
from.serializers import AnswaresSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .customLibs.connect_database import ConnectDatabase
from .customLibs.servicos_orgaos import ServicosOrgaos
import time


class AnswaresViewSet(viewsets.ModelViewSet):
    queryset = Answares.objects.all()
    serializer_class = AnswaresSerializer

    def update(self, request, *args, **kwargs):
        #alterar: lime_id, servico_id, servico_nome, status
        instance = self.get_object()
        servicos = ServicosOrgaos.returnServicos()
        if not self.request.data['servico_nome'] in servicos:
            # fazer post para nova ID de serviço
            pass
        
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
        # print(atual)
        # if horario_atual - horario_banco > 1h:
        survey = '311832'
        newAnswares = ConnectDatabase.queryAnswerServiceOther(survey)
        servicos_orgaos = ServicosOrgaos.returnOrgaos()
        for answare in newAnswares:
            try:
                id_orgao = int(answare[survey + 'X1X1'])
                if answare[survey + 'X1X3'] == '-oth-':
                    nome_servico = answare[survey + 'X1X3other']
                    id_servico = '0000'
                    answare_id = str(survey) + str(answare['id'])
                else:
                    continue
                orgao_nome = servicos_orgaos[str(id_orgao)][0]['orgao_nome']
                survey_id = int(survey)
                lime_id = int(str(id_orgao) + id_servico)
                Answares.objects.create(
                    answare_id = int(answare_id),
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

