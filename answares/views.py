# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .models import Answares
from.serializers import AnswaresSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



class AnswaresViewSet(viewsets.ModelViewSet):
    queryset = Answares.objects.all()
    serializer_class = AnswaresSerializer

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
        pendings = Answares.objects.filter(status='S')
        serializer = AnswaresSerializer(pendings, many=True, context={'request': request})
        return Response(serializer.data)
