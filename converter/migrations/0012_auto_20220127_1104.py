# Generated by Django 2.2 on 2022-01-27 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0011_auto_20220127_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.today, null=True, verbose_name='Дата'),
        ),
    ]
