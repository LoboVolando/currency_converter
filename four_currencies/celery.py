from __future__ import absolute_import, unicode_literals
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'four_currencies.settings')
django.setup()

from celery import Celery
from celery.schedules import crontab
import time
import datetime
import requests
import logging
from converter.models import Rate


logger = logging.Logger('Celery_logger', level=logging.DEBUG)
handler_1 = logging.FileHandler('celery.log')
handler_2 = logging.StreamHandler()
logger.addHandler(handler_1),
logger.addHandler(handler_2)


api = 'f1f3cd1115354997b6ec29dffcd66ff7'


app = Celery('four_currencies')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def set_periodic(sender, **kwrags) -> None:
    """
    Функция запуска периодической задачи
    :param sender:
    :param kwrags:
    """
    sender.add_periodic_task(
        crontab(hour=13, minute=10),
        # check_updates.s()
        fill_db.s()
    )


@app.task
def check_updates() -> None:
    """
    Функция ежедневного добавления строки записи обменных курсов в БД.
    """

    r = requests.Session()
    path = f'https://openexchangerates.org/api/latest.json?app_id={api}&symbols=EUR,PLN,CZK'

    data = r.get(path).json()
    date = datetime.datetime.today()

    logger.info(f"{data['rates']['EUR']}, {data['rates']['PLN']}, {data['rates']['CZK']}")
    Rate.objects.create(eur=data['rates']['EUR'], pln=data['rates']['PLN'], czk=data['rates']['CZK'], date=date)
    logger.debug('Saved')


@app.task
def fill_db() -> None:
    """
    Функция начального заполнения БД записями обменных курсов
    """

    dates = [datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=index), '%Y-%m-%d')
             for index in range(26, 0, -1)]
    for date in dates:
        print('Request sent')
        r = requests.Session()
        path = f'https://openexchangerates.org/api/historical/{date}.json?app_id={api}&symbols=EUR,PLN,CZK'

        data = r.get(path).json()

        logger.info(f"{data['rates']['EUR']}, {data['rates']['PLN']}, {data['rates']['CZK']}")
        Rate.objects.create(eur=data['rates']['EUR'], pln=data['rates']['PLN'], czk=data['rates']['CZK'], date=date)
        logger.debug('Saved')

        time.sleep(5)
