import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tob_jobs2.settings')

app = Celery('root')

app.conf.broker_connection_retry_on_startup = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
