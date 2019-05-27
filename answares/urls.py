from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from .views import PendingsList, ProcessedsList, AnswaresViewSet, OrgaoViewSet, ServicoViewSet, Sugestoes
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'answares',AnswaresViewSet)
router.register(r'orgao',OrgaoViewSet)
router.register(r'servico',ServicoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('pendings/', PendingsList.as_view()),
    path('processeds/', ProcessedsList.as_view()),
    path('sugestoes/', Sugestoes.as_view({'post': 'post'})),
    # path('answares/', AnswaresViewSet.as_view({'put':'update'})),

    # path('servicos/', ServicosList.as_view({'get': 'get'})),
    # path('orgaos/', OrgaosList.as_view({'get': 'get'})),
]
