from django.http import HttpResponse
from django.shortcuts import render
from .forms import ExchangeForm
from .models import Rate
from .serializers import RateSerializer
from datetime import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin


def report(request):
    """
    Функция представления страницы конвертации валют
    :param request: принимает запрос
    :return: возвращает рендер шаблона с формой и результатами обработки формы
    """
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
            date = form.cleaned_data['date']

            if date > date.today():
                form.add_error('__all__', 'Error. Date is from the future')
            else:
                if date == date.today():
                    rate = Rate.objects.last()
                else:
                    rate = Rate.objects.filter(date=date)[0]

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
            form.add_error('__all__', 'Form is not valid. Quantity seems to be empty')

    return render(request, 'converter/report.html', {'form': form,
                                                     'date': date,
                                                     'result': result,
                                                     'exchange_rate': exchange_rate})


class RateList(GenericAPIView, ListModelMixin):
    """
    Класс предоставления по API списка курсов
    При передаче в строке запроса аргументов from=дата, to=дата возвращает список
    за промежуток указанных дат
    """
    serializer_class = RateSerializer

    def get_queryset(self):
        queryset = Rate.objects.all()
        start_date = self.request.query_params.get('from')
        end_date = self.request.query_params.get('to')

        if start_date and end_date:
            queryset = queryset.filter(date__gte=start_date).filter(date__lte=end_date)
        return queryset

    def get(self, request):
        return self.list(request)


class RateDetail(GenericAPIView, RetrieveModelMixin):
    """
    Класс предоставления по API списка курсов на конкретную дату
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    lookup_field = 'date'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
