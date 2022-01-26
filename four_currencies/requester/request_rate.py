import datetime

import requests
from decouple import config
# from converter.models import Rate

# api = config("API_KEY")
api = 'f1f3cd1115354997b6ec29dffcd66ff7'


def check_updates() -> None:
    """
    Отправляет тестовые запросы. Если появились новые предложения, порог поиска сдвигается
    :return:
    """

    r = requests.Session()
    path = f'https://openexchangerates.org/api/latest.json?app_id={api}&symbols=EUR,PLN,CZK'

    data = r.get(path).json()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # rate = Rate(date, data['rates']['EUR'], data['rates']['PLN'], data['rates']['CZK'])
    # rate.save()
    print(date, data['rates']['EUR'], data['rates']['PLN'], data['rates']['CZK'])


if __name__ == "__main__":
    check_updates()
