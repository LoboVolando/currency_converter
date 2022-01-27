import datetime

from django import forms

CURRENCY_CHOICES = [('USD', 'USD'), ('EUR', 'EUR'), ('PLN', 'PLN'), ('CZK', 'CZK')]


class ExchangeForm(forms.Form):
    """
    Форма запроса расчета суммы обмена между валютами USD, EUR, PLN, CZK
    """
    quantity = forms.DecimalField(min_value=0, max_value=1000000, help_text='Put some number here')
    date = forms.DateField(widget=forms.SelectDateWidget())
    from_cur = forms.ChoiceField(choices=CURRENCY_CHOICES)
    to_cur = forms.ChoiceField(choices=CURRENCY_CHOICES)
