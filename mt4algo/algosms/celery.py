from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algosms.settings')

app = Celery('algosms')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algosms.settings')

app = Celery('algosms')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
