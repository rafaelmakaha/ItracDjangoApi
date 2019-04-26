from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from .views import PendingsList, ProcessedsList, AnswaresViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'answares',AnswaresViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('pendings/', PendingsList.as_view()),
    path('processeds/', ProcessedsList.as_view()),
]
