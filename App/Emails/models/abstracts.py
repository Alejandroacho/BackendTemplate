from abc import abstractmethod

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from App.utils import log_information


class AbstractEmailFunctionClass(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id} | {self.subject}'

    @abstractmethod
    def get_emails(self):
        raise ValueError('Abstract method, must be implemented in child class')

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

    def check_if_email_is_in_blacklist(self):
        blacklist = apps.get_model('Emails', 'Blacklist')
        is_email_in_blacklist = blacklist.objects.filter(
            email__in=self.get_emails()
        ).exists()
        return is_email_in_blacklist

    def send(self):
        is_email_in_blacklist = self.check_if_email_is_in_blacklist()
        if not is_email_in_blacklist:
            email = self.get_email_object()
            email.send()
            self.sent_date = timezone.now()
            self.was_sent = True
            self.save()
            log_information('sent', self)
        else:
            raise ValueError('Email is in blacklist')


class AbstractEmailClass(AbstractEmailFunctionClass):
    header = models.CharField(max_length=100, null=True)
    sent_date = models.DateTimeField(null=True)
    was_sent = models.BooleanField(default=False, editable=False)
    blocks = models.ManyToManyField(
        'Emails.Block', related_name='%(class)s_blocks'
    )
