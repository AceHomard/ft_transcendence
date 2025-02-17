from django.db import models


class TransactionId(models.Model):
    transaction_id = models.BigIntegerField()