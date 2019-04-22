from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('api/', include([
        path('answares/', include('answares.urls')),
    ])),
]
