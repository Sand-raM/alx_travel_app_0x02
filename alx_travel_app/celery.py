
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')

# Configure Celery using Django settings with a 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
        print(f'Request: {self.request!r}')

