from django.db import models
from django.contrib.postgres.fields import ArrayField


class TransactionId(models.Model):
    transaction_id = models.BigIntegerField()
