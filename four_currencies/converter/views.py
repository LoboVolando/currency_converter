from django.http import HttpResponse
from django.shortcuts import render
from .forms import ExchangeForm
from converter.models import Rate
from datetime import datetime


def report(request):
    date = datetime.now().strftime('%Y-%m-%d')
    form = ExchangeForm()
    result = 0
    exchange_rate = None

    if request.method == 'POST':
        form = ExchangeForm(request.POST)

        if form.is_valid():
            from_cur = form.cleaned_data['from_cur']
            to_cur = form.cleaned_data['to_cur']
            quantity = form.cleaned_data['quantity']
            exchange_rate = 1

            rate = Rate.objects.last()
            if from_cur == to_cur:
                exchange_rate = 1

            elif from_cur == 'USD':
                if to_cur == 'EUR':
                    exchange_rate = rate.eur
                elif to_cur == 'PLN':
                    exchange_rate = rate.pln
                else:
                    exchange_rate = rate.czk

            elif from_cur == 'EUR':
                if to_cur == 'USD':
                    exchange_rate = 1 / rate.eur
                elif to_cur == 'PLN':
                    exchange_rate = rate.pln / rate.eur
                else:
                    exchange_rate = rate.czk / rate.eur

            elif from_cur == 'PLN':
                if to_cur == 'USD':
                    exchange_rate = 1 / rate.pln
                elif to_cur == 'EUR':
                    exchange_rate = rate.eur / rate.pln
                else:
                    exchange_rate = rate.czk / rate.pln

            else:
                if to_cur == 'USD':
                    exchange_rate = 1 / rate.czk
                elif to_cur == 'EUR':
                    exchange_rate = rate.eur / rate.czk
                else:
                    exchange_rate = rate.pln / rate.czk

            exchange_rate = round(exchange_rate, 2)
            result = round(quantity * exchange_rate, 2)
            return render(request, 'converter/report.html', {'form': form,
                                                             'date': date,
                                                             'result': result,
                                                             'exchange_rate': exchange_rate})

        else:
            return HttpResponse('Form is not valid')
    return render(request, 'converter/report.html', {'form': form,
                                                     'date': date,
                                                     'result': result,
                                                     'exchange_rate': exchange_rate})
