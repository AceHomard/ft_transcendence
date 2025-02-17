from django.db import models


# Create your models here.
class TransactionId(models.Model):
    transaction_id = models.BigIntegerField()
