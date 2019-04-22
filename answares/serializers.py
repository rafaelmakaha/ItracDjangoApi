from rest_framework import serializers
from .models import Answares


class AnswaresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answares
        fields = '__all__'
