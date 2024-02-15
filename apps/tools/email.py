from django.conf import settings
from django.core.mail import send_mail


def send_email_tool(title: str, body, to_emails: tuple):
    send_mail(
        title,
        body,
        settings.EMAIL_HOST_USER,
        to_emails,
        fail_silently=False,
    )
