from django.db import models

class Answares(models.Model):
    servico_id = models.IntegerField()
    servico_nome = models.CharField(
        max_length=120
    )
    orgao_id = models.IntegerField()
    orgao_nome = models.CharField(
        max_length=120
    )