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
