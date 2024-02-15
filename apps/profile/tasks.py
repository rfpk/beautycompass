import logging
from config.celery_settings import app
from django.db.models import Max, F
from django.utils import timezone
from .models import Author, AuthorHistory
from apps.tools.email import send_email_tool


logger = logging.getLogger('tasks')


@app.task(max_retries=1, default_retry_delay=5)
def check_author_status():
    today = timezone.now().date()
    authors = Author.objects.annotate(last_history=Max('history__created_at')).prefetch_related('history')\
        .filter(
        history__current_status='BU',
        history__close_at=today,
        history__created_at=F('last_history')
    )
    for author in authors:
        AuthorHistory.objects.create(author=author, created_at=today)
        logger.info(f'New status for author: {author}')


@app.task(max_retries=1, default_retry_delay=5)
def send_email_task(body_text, send_email_profile):
    send_email_tool('Title', body_text, (send_email_profile, ))
