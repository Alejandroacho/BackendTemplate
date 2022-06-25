from abc import abstractmethod
from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Model
from django.db.models.fields import Field
from django.template.loader import render_to_string
from django.utils import timezone
from Emails.choices import EmailAffair
from Project.utils import log_information


class AbstractEmailFunctionClass(Model):
    class Meta:
        abstract: bool = True

    def __str__(self) -> str:
        return f"{self.id} | {self.subject}"

    @abstractmethod
    def get_emails(self) -> list:
        raise ValueError("Abstract method, must be implemented in child class")

    def get_email_data(self) -> dict:
        return {
            "header": self.header,
            "blocks": self.blocks.all() if self.blocks.all() else [],
        }

    def get_template(self) -> str:
        data: dict = self.get_email_data()
        template: str = render_to_string("email.html", data)
        return template

    def get_email_object(self) -> EmailMultiAlternatives:
        email: EmailMultiAlternatives = EmailMultiAlternatives(
            subject=self.subject,
            from_email=settings.EMAIL_HOST_USER,
            bcc=self.get_emails(),
        )
        email.attach_alternative(self.get_template(), "text/html")
        email.fail_silently = False
        return email

    def check_if_email_is_in_blacklist(self) -> bool:
        blacklist: Model = apps.get_model("Emails", "Blacklist")
        is_email_in_blacklist: bool = blacklist.objects.filter(
            email__in=self.get_emails()
        ).exists()
        return is_email_in_blacklist

    def send(self) -> None:
        is_email_in_blacklist: bool = self.check_if_email_is_in_blacklist()
        if not is_email_in_blacklist:
            email: EmailMultiAlternatives = self.get_email_object()
            email.send()
            self.sent_date: datetime = timezone.now()
            self.was_sent: bool = True
            self.save()
            log_information("sent", self)
        else:
            raise ValueError("Email is in blacklist")


class AbstractEmailClass(AbstractEmailFunctionClass):
    header: Field = models.CharField(max_length=100, null=True)
    affair: Field = models.CharField(
        max_length=100,
        choices=EmailAffair.choices,
        default=EmailAffair.NOTIFICATION.value,
    )
    sent_date: Field = models.DateTimeField(null=True)
    was_sent: Field = models.BooleanField(default=False, editable=False)
    blocks: Field = models.ManyToManyField(
        "Emails.Block", related_name="%(class)s_blocks"
    )
