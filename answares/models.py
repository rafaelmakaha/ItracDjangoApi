from django.db import models

class Answares(models.Model):

    STATUS_TYPE = (
        ('P', 'Processed'),
        ('N', 'Not Processed')
    )

    answare_id = models.IntegerField(
        primary_key=True
    )
    lime_id = models.IntegerField()
    survey_id = models.IntegerField()
    servico_id = models.IntegerField()
    servico_nome = models.CharField(
        max_length=120
    )
    orgao_id = models.IntegerField()
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