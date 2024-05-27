import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    'check_activity': {
        'task': 'users.tasks.check_activity',
        'schedule': timedelta(minutes=1),
    },
    'habits_reminder': {
            'task': 'habit.tasks.habits_reminder',
            'schedule': timedelta(minutes=1),
        },
}
