from django.db import models

class Answares(models.Model):

    STATUS_TYPE = (
        ('P', 'Processed'),
        ('N', 'Not Processed')
    )

    answare_id = models.CharField(
        primary_key=True,
        max_length=120
    )
    lime_id = models.CharField(max_length=120)
    survey_id = models.CharField(max_length=120)
    servico_id = models.CharField(max_length=120)
    servico_nome = models.CharField(max_length=400)
    orgao_id = models.CharField(max_length=12)
    orgao_dbid = models.CharField(max_length=12, default="-1")
    tipo_solicitante = models.CharField(max_length=120, null=True)
    titulo_etapa = models.CharField(max_length=120, null=True)
    tempo_total_estimado_dias = models.CharField(max_length=50, default="-1")

    orgao_nome = models.CharField(
        max_length=120
    )
    status = models.CharField(
        default='N',
        max_length=1,
        choices=STATUS_TYPE
    )

class Orgao(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12
    )
    dbid = models.CharField(
        max_length=12,
        default='0'
    )
    nome = models.CharField(
        max_length=200
    )


class Servico(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12
    )
    nome = models.CharField(
        max_length=200
    )
    orgao = models.ForeignKey(
        'Orgao',
        related_name='servico',
        on_delete=models.CASCADE
    )

class Horario(models.Model):
    last_time = models.TimeField()