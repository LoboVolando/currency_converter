# Generated by Django 2.2 on 2022-01-27 01:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0005_auto_20220127_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата'),
        ),
    ]
