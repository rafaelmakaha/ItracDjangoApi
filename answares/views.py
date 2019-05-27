# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import pickle
import json
from datetime import datetime, timedelta

import requests
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action

from answares.auth_data import username, password, servicos_username, servicos_password
from .models import Answares, Horario, Orgao, Servico
from .serializers import AnswaresSerializer, ServicoSerializer, OrgaoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .customLibs.connect_database import ConnectDatabase
from .customLibs.servicos_orgaos import ServicosOrgaos
import time
import re
from Levenshtein.StringMatcher import distance

picke_timefile = "last_refresh.pickle"
survey = '396326'


def save_time():
    last_refresh = {"last_refresh": datetime.now()}

    pickle_out = open(picke_timefile, "wb")
    pickle.dump(last_refresh, pickle_out)
    pickle_out.close()


def get_time():
    tnow = None
    if os.path.isfile(picke_timefile):
        with open(picke_timefile, "rb") as pickle_in:
            try:
                last_refresh = pickle.load(pickle_in)
                tnow = last_refresh['last_refresh']
            except Exception:  # so many things could go wrong, can't be more specific.
                pass

    return tnow


def parse_answer(inputdict, keypart, criteria):
    listresult = [{key:value} for key, value in inputdict.items() if keypart in key and value==criteria]
    answers = []
    for l in listresult:
        m = re.search(r"\[(.*)\]", next(iter(l)))
        answers.append(m.group(1))
    return answers


class Sugestoes(viewsets.ModelViewSet):

    def post(self, request, format=None):
        nome = self.request.data['nome']
        qtd = 5
        all_servicos = Servico.objects.all()

        list_result = []
        for s in all_servicos:
            distancia = distance(nome, s.nome)
            list_result.append({'distance': distancia, 'nome': s.nome})

        sorted_list = sorted(list_result, key=lambda i: i['distance'])
        return Response({"sugestoes": sorted_list[1:qtd + 1]})


class AnswaresViewSet(viewsets.ModelViewSet):
    queryset = Answares.objects.all()
    serializer_class = AnswaresSerializer

    def update(self, request, *args, **kwargs):
        servicos = Servico.objects.values_list('nome', flat=True)
        if not self.request.data['servico_nome'] in servicos:
            ans = Answares.objects.get(pk=self.request.data['answare_id'])
            ans.servico_nome = self.request.data['servico_nome']
            response = ServicosOrgaos.create_servico(ans.__dict__, servicos_username, servicos_password)
            servico_id = response.json()['resposta']
            try:
                ans.servico_id = servico_id
                ans.save()
            except Answares.DoesNotExist:
                pass
        else:
            servico_id = self.request.data['servico_id']

        try:
            survey_id = self.request.data['survey_id']
            answare_id = self.request.data['answare_id']
            answare_id = ''.join(answare_id.split(survey_id))
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
        last_bdrefresh = get_time()
        diff = timedelta(hours=2)
        if last_bdrefresh:
            diff = datetime.now() - last_bdrefresh

        refresh = diff > timedelta(hours=1)
        if refresh:
            orgaos = ServicosOrgaos.returnOrgaosObjects()
            save_time()
            for orgao in orgaos:
                try:
                    Orgao.objects.create(
                        id=orgao['id'],
                        nome=orgao['nome'],
                        dbid=orgao['dbid']
                    )
                except Exception as e:
                    pass

                for servico in orgao['servicos']:
                    try:
                        parent = Orgao.objects.get(id=orgao['id'])
                        Servico.objects.create(
                            id=servico['id'],
                            nome=servico['nome'],
                            orgao=parent
                        )
                    except Exception as e:
                        pass

        newAnswares = ServicosOrgaos.getLimesureveyAnswers(survey, username, password)
        for answare in newAnswares:
            id_nome_orgao = answare['A qual instituição você pertence?'].split('-')
            if len(id_nome_orgao) <= 1:
                continue

            id_orgao = id_nome_orgao[1].strip().zfill(8)
            if not id_orgao.isdigit():
                continue
            if answare['Informe o nome do serviço que será avaliado nessa pesquisa.'] == 'Outros':
                nome_servico = answare['Informe o nome do serviço que será avaliado nessa pesquisa. [Outros]']
                id_servico = '0000'
                answare_id = survey + str(answare['ID da resposta'])
            else:
                continue

            orgao_nome = id_nome_orgao[0].strip()
            tipo_solicitante_tmp = parse_answer(answare, 'O serviço\xa0é oferecido a pessoas físicas, jurídicas ou ambas?', 'Sim')

            if 'Ambas' in tipo_solicitante_tmp:
                tipo_solicitante = [{"tipo": "Pessoa Física"}, {"tipo": "Pessoa Jurídica"}]
            else:
                tipo_solicitante = [{"tipo": "Pessoa {0}".format(i)} for i in tipo_solicitante_tmp if i != 'Ambas']

            titulo_etapa = ""
            tempo_total_estimado_dias = answare['Quantos dias o usuário espera até a efetiva entrega do serviço?']
            if not tempo_total_estimado_dias:
                tempo_total_estimado_dias="-1"
            survey_id = survey
            lime_id = id_orgao + id_servico

            try:
                Answares.objects.create(
                    answare_id=answare_id,
                    lime_id=lime_id,
                    survey_id=survey_id,
                    servico_id=id_servico,
                    orgao_id=id_orgao,
                    orgao_nome=orgao_nome,
                    servico_nome=nome_servico,
                    status="N",
                    tipo_solicitante=json.dumps(tipo_solicitante),
                    titulo_etapa=titulo_etapa,
                    tempo_total_estimado_dias=tempo_total_estimado_dias,
                )
            except Exception as e:
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
