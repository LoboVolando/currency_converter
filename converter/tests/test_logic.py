# from django.contrib.auth.models import User
import datetime
import json

from django.test import TestCase
from django.shortcuts import render
from converter.models import Rate
from converter.forms import ExchangeForm
from four_currencies.celery import check_updates


class TestView(TestCase):
    def test_view_exists(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'converter/report.html')

    def test_view_response_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_includes(self):
        response = self.client.get('/')
        self.assertContains(response, 'Result')


class TestApiList(TestCase):
    @classmethod
    def setUp(cls):
        for date, pln in [('2022-01-25', 4),
                          ('2022-01-26', 8),
                          ('2022-01-27', 4),
                          ('2022-01-28', 8),
                          ('2022-01-29', 4.25)]:

            Rate.objects.create(
                eur=0.88,
                pln=pln,
                czk=20.15,
                date=date
            )

    def test_list_response(self):
        response = self.client.get('/api/ratelist')
        self.assertEqual(response.status_code, 301)

    def test_view_includes(self):
        response = self.client.get('/api/ratelist/')
        print(response.data[1]['date'])
        self.assertEqual(response.data[0]['date'], '2022-01-25')
        self.assertEqual(len(response.data), 5)

    def test_view_specific_date(self):
        date = '2022-01-29'
        response = self.client.get(f'/api/rate/{date}')
        self.assertEqual(response.data['date'], date)
        self.assertEqual(float(response.data['pln']), 4.25)

    def test_check_updates(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        check_updates()
        response = self.client.get('/api/ratelist/')
        self.assertEqual(len(response.data), 6)

        response = self.client.get(f'/api/rate/{today}')
        self.assertEqual(response.data['date'], today)

    def test_currency_conversion(self):
        form = ExchangeForm(
            data={'date': '2022-01-26',
                  'from_cur': 'USD',
                  'to_cur': 'PLN',
                  'quantity': 1500}
        )

        response = self.client.post('/', data=form, content_type='application/json')
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
