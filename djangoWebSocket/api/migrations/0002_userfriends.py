# Generated by Django 5.0.3 on 2024-06-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFriends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
    ]
