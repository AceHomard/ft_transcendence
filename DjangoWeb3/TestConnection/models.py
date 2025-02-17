from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class Tournament(models.Model):
    match_ids = ArrayField(models.BigIntegerField(), default=list)
    tournament_id = models.BigIntegerField()
    timestamps = ArrayField(models.BigIntegerField(), default=list)
    player1_scores = ArrayField(models.BigIntegerField(
            validators=[MinValueValidator(limit_value=0),
                        MaxValueValidator(limit_value=255)]), default=list)
    player2_scores = ArrayField(models.BigIntegerField(
            validators=[MinValueValidator(limit_value=0),
                        MaxValueValidator(limit_value=255)]), default=list)
    player1_ids = ArrayField(models.BigIntegerField(), default=list)
    player2_ids = ArrayField(models.BigIntegerField(), default=list)
    winner_ids = ArrayField(models.BigIntegerField(), default=list)


class Match(models.Model):
    match_id = models.BigIntegerField()
    tournament_id = models.BigIntegerField()
    timestamp = models.BigIntegerField()
    player1_score = models.BigIntegerField()
    player2_score = models.BigIntegerField()
    player1_id = models.BigIntegerField()
    player2_id = models.BigIntegerField()
    winner_id = models.BigIntegerField()


class TxHash(models.Model):
    match_id = models.BigIntegerField(blank=True, null=True)
    tournament_id = models.BigIntegerField(blank=True, null=True)
    tx_hash = models.CharField(max_length=255)


class TransactionId(models.Model):
    transaction_id = models.BigIntegerField()
