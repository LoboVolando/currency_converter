import datetime
from django.utils import timezone
from django.db import models


class Rate(models.Model):
    """
    Модель записи в бд обменных курсов на конкретную дату
    """
    date = models.DateField(blank=True, null=True, default=datetime.datetime.today, verbose_name='Дата')
    eur = models.DecimalField(null=True, verbose_name='euro', decimal_places=5, max_digits=8)
    pln = models.DecimalField(null=True, verbose_name='zloty', decimal_places=5, max_digits=8)
    czk = models.DecimalField(null=True, verbose_name='krona', decimal_places=5, max_digits=8)
