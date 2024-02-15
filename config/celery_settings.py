from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue
from celery.schedules import crontab
from datetime import timedelta


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Setup django project
# django.setup()
CELERY_RESULT_BACKEND = 'django-db'
RABBIT_HOSTNAME = os.environ.get('RABBITMQ_DEFAULT_HOSTNAME', 'localhost')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]


BROKER_URL = 'amqp://localhost'
# BROKER_URL = 'redis://localhost:6379'


# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10

CELERY_DEFAULT_QUEUE = 'default'

CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
# CELERY_IGNORE_RESULT = True

app = Celery('config', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, result_backend='rpc://',
             include=['apps.profile.tasks', ])

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

CELERYCAM_EXPIRE_SUCCESS = timedelta(days=1)
CELERYCAM_EXPIRE_ERROR = timedelta(days=3)
CELERYCAM_EXPIRE_PENDING = timedelta(days=5)

app.conf.task_default_queue = 'tasks'
app.conf.broker_connection_retry_on_startup = True

app.conf.task_default_priority = 5
app.conf.task_queues = (
    Queue('tasks', Exchange('tasks'), routing_key='tasks'),
    Queue('schedule_tasks', Exchange('schedule_tasks'), routing_key='schedule_tasks'),
)

app.conf.task_routes = {
    'apps.profile.tasks.send_email_task': {
        'queue': 'tasks',
    },
    'apps.profile.tasks.check_author_status': {
        'queue': 'schedule_tasks',
    },
}

app.conf.beat_schedule = {
    'check_author_status': {
        'task': 'apps.profile.tasks.check_author_status',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },

    'check_product_status': {
        'task': 'apps.products.tasks.check_product_status',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },

}

# launch command:
# celery -A config.celery_settings worker -O fair -Q tasks --concurrency=1 -n tasks
# celery -A config.celery_settings worker -O fair -Q schedule_tasks --concurrency=1 -n schedule_tasks -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
