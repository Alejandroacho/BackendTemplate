from datetime import datetime

from celery import shared_task
from django.db.models import QuerySet
from django.utils import timezone
from Emails.models.models import Email
from Project.celery_worker.worker import app


SECONDS: float = 10.0


@shared_task
def send_emails() -> None:
    now: datetime = timezone.now()
    emails: QuerySet = Email.objects.filter(
        was_sent=False, programed_send_date__lte=now
    )
    for email in emails:
        email.send()


def each_seconds() -> float:
    return SECONDS


app.conf.beat_schedule = {
    "send_emails": {
        "task": "Emails.tasks.send_emails",
        "schedule": each_seconds(),
    },
}
