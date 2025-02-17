# Generated by Django 5.0.3 on 2024-05-30 14:06

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.BigIntegerField()),
                ('tournament_id', models.BigIntegerField()),
                ('timestamp', models.BigIntegerField()),
                ('player1_score', models.BigIntegerField()),
                ('player2_score', models.BigIntegerField()),
                ('player1_id', models.BigIntegerField()),
                ('player2_id', models.BigIntegerField()),
                ('winner_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_ids', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), default=list, size=None)),
                ('tournament_id', models.BigIntegerField()),
                ('timestamps', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), default=list, size=None)),
                ('player1_scores', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=255)]), default=list, size=None)),
                ('player2_scores', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=255)]), default=list, size=None)),
                ('player1_ids', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), default=list, size=None)),
                ('player2_ids', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), default=list, size=None)),
                ('winner_ids', django.contrib.postgres.fields.ArrayField(base_field=models.BigIntegerField(), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TxHash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.BigIntegerField(blank=True, null=True)),
                ('tournament_id', models.BigIntegerField(blank=True, null=True)),
                ('tx_hash', models.CharField(max_length=255)),
            ],
        ),
    ]
