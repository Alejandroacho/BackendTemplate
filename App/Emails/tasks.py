from celery import shared_task
from django.utils import timezone

from App.celery.worker import app
from Emails.models.models import Email


SECONDS = 10.0


@shared_task
def send_emails():
    now = timezone.now()
    emails = Email.objects.filter(was_sent=False, programed_send_date__lte=now)
    for email in emails:
        email.send()


def each_seconds():
    return SECONDS


app.conf.beat_schedule = {
    'send_emails': {
        'task': 'Emails.tasks.send_emails',
        'schedule': each_seconds(),
    },
}
