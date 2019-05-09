# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .models import Answares
from.serializers import AnswaresSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .customLibs.connect_database import ConnectDatabase
from .customLibs.servicos_orgaos import ServicosOrgaos


class AnswaresViewSet(viewsets.ModelViewSet):
    queryset = Answares.objects.all()
    serializer_class = AnswaresSerializer
    def get(self, request, format=None):
        


        answares = Answares.objects.all()
        serializer = AnswaresSerializer(answares, many=True, context={'request': request})
        return Response(serializer.data)

class PendingsList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        try:
            survey = '311832'
            newAnswares = ConnectDatabase.queryAnswerServiceOther(survey)
            servicos_orgaos = ServicosOrgaos.returnOrgaos()
            for answare in newAnswares:
                id_orgao = int(answare[6])
                if answare[8] == '-oth-':
                    nome_servico = answare[9]
                    id_servico = 0000
                else:
                    continue
                    id_servico = answare[8]
                servicos_orgaos[int(id_orgao)][0]['orgao_nome']
                survey_id = int(survey)
                lime_id = int(id_orgao + '0000')
                Answares.objects.create(
                    lime_id=lime_id,
                    survey_id=survey_id,
                    servico_id=id_servico,
                    orgao_id=id_orgao,
                    orgao_nome="",
                    servico_nome="",
                    status="N"
                )
        except:
            print('Não foi possível atualizar o banco')
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

