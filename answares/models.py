from django.db import models

class Answares(models.Model):

    STATUS_TYPE = (
        ('P', 'Processed'),
        ('N', 'Not Processed')
    )


    lime_id = models.IntegerField(
        primary_key=True
    )
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