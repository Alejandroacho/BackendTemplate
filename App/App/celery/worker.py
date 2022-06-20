from celery import Celery
from django.conf import settings


app = Celery('App', broker='redis://localhost:6379/0')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
