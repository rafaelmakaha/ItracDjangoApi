from rest_framework import serializers
from .models import Answares


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

class ServicosSerializer(serializers.Serializer):
    servico_nome = serializers.CharField()
    servico_id = serializers.CharField()

class OrgaosSerializer(serializers.Serializer):
    orgao_nome = serializers.CharField()
    orgao_id = serializers.CharField()