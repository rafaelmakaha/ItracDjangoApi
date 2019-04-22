# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .models import Answares
from.serializers import AnswaresSerializer


class AnswaresViewSet(viewsets.ModelViewSet):
    queryset = Answares.objects.all()
    serializer_class = AnswaresSerializer