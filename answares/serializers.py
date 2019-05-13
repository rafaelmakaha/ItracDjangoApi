from rest_framework import serializers
from .models import Answares, Orgao, Servico


class AnswaresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answares
        fields = (
            'answare_id',
            'lime_id',
            'survey_id',
            'servico_id',
            'servico_nome',
            'orgao_id',
            'orgao_nome',
            'status',
            'url'
        )

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = (
            'id',
            'nome',
            'url',
            'orgao'
        )

class OrgaoSerializer(serializers.ModelSerializer):
    servico = ServicoSerializer(many=True, read_only=True)
    class Meta:
        model = Orgao
        fields = (
            'id',
            'nome',
            'url',
            'servico'
        )