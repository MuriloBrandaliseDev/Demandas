# Generated by Django 5.1.1 on 2025-01-06 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_membro_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='data_demanda',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Data da Demanda'),
        ),
    ]