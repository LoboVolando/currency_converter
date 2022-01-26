from django.urls import path
from converter.views import report

app_name = 'converter'

urlpatterns = [
    path('', report, name='report'),
]