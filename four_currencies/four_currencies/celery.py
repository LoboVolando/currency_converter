import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_supper_app.settings')
app = Celery('four_currencies')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
