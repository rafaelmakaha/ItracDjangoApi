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
        survey = '311832'
        newAnswares = ConnectDatabase.queryAnswerServiceOther(survey)
        servicos_orgaos = ServicosOrgaos.returnOrgaos()

        for element in newAnswares:
            for key in servicos_orgaos:
                if element[6] == servicos_orgaos[key][0]['orgao_nome']:
                    pass


        answares = Answares.objects.all()
        serializer = AnswaresSerializer(answares, many=True, context={'request': request})
        return Response(serializer.data)

class PendingsList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
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
