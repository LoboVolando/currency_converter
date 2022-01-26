from django.db import models


class Rate(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    eur = models.DecimalField(verbose_name='euro', decimal_places=5, max_digits=8)
    pln = models.DecimalField(verbose_name='zloty', decimal_places=5, max_digits=8)
    czk = models.DecimalField(verbose_name='krona', decimal_places=5, max_digits=8)
