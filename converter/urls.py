from django.urls import path
from converter.views import report, RateList, RateDetail

app_name = 'converter'

urlpatterns = [
    path('', report, name='report'),
    path('api/ratelist/', RateList.as_view(), name='rate_list'),
    path('api/rate/<date>', RateDetail.as_view(), name='rate_detail'),

]
