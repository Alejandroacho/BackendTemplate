from abc import abstractmethod

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from App.utils import log_information


class AbstractEmailClass(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id} | {self.subject}'

    @abstractmethod
    def get_emails(self):
        pass

    def get_email_data(self):
        return {
            'header': self.header,
            'blocks': self.blocks.all() if self.blocks.all() else [],
        }

    def get_template(self):
        data = self.get_email_data()
        template = render_to_string('email.html', data)
        return template

    def get_email_object(self):
        email = EmailMultiAlternatives(
            subject=self.subject,
            from_email=settings.EMAIL_HOST_USER,
            bcc=self.get_emails(),
        )
        email.attach_alternative(self.get_template(), 'text/html')
        email.fail_silently = False
        return email

    def send(self):
        email = self.get_email_object()
        email.send()
        self.sent_date = timezone.now()
        self.was_sent = True
        self.save()
        log_information('sent', self)