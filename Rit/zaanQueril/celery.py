# celery.py
from __future__  import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zaanQueril.settings')

app = Celery('zaanQueril')
app.conf.broker_connection_retry_on_startup = True

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()

# myproject/celery.py


# app.conf.beat_schedule = {
#     'distribute-roi-every-day-midnight': {
#         'task': 'zqUsers.tasks.distribute_roi',
#         'schedule': crontab(minute=30, hour=18),  # At 00:00 (midnight) UTC every day
#         # 'schedule': 10,  # At 00:00 (midnight) UTC every day
#         # 'schedule': 86400,
#     },
# }

