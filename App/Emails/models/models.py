from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from Emails import factories
from Emails.choices import CommentType
from Emails.models.abstracts import AbstractEmailClass
from Users.fakers.user import EmailTestUserFaker
from Users.models import User


class Block(models.Model):
    """
    Block model used on email as block content
    """

    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    show_link = models.BooleanField(default=False)
    link_text = models.CharField(max_length=100, null=True)
    link = models.URLField(max_length=100, null=True)

    def __str__(self):
        return f'{self.id} | {self.title}'


class Email(AbstractEmailClass):
    """
    Email model
    """

    subject = models.CharField(max_length=100)
    is_test = models.BooleanField(default=False)
    programed_send_date = models.DateTimeField(null=True)
    to = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='to_user'
    )

    def get_emails(self):
        return [self.to.email]

    def set_programed_send_date(self):
        programmed_date = self.programed_send_date
        if programmed_date and programmed_date <= timezone.now():
            message = 'Programed send date must be future'
            raise ValidationError(message, code='invalid')
        if not programmed_date:
            five_minutes_ahead = timezone.now() + timezone.timedelta(minutes=5)
            self.programed_send_date = five_minutes_ahead

    def save(self, *args, **kwargs):
        if self.is_test:
            self.to = EmailTestUserFaker()
        self.set_programed_send_date()
        super(Email, self).save(*args, **kwargs)


class Suggestion(AbstractEmailClass):
    """
    Suggestion model, emails that will be sent to admin suggestions email
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='suggestion', unique=False
    )
    subject = models.CharField(
        max_length=100,
        choices=CommentType.choices,
        default=CommentType.SUGGESTION.value,
    )
    was_read = models.BooleanField(default=False)

    def get_emails(self):
        return [settings.SUGGESTIONS_EMAIL]


class Notification(AbstractEmailClass):
    """
    Notification model, it creates an email for each user with this data
    """

    subject = models.CharField(max_length=100)
    is_test = models.BooleanField(default=False)
    programed_send_date = models.DateTimeField(null=True)

    def send(self):
        if self.is_test:
            self.create_email(to=EmailTestUserFaker())
        else:
            for user in User.objects.all():
                self.create_email(user)
        self.sent_date = timezone.now()
        self.was_sent = True
        self.save()

    def create_email(self, to):
        factories.email.EmailFactory(
            to=to,
            subject=self.subject,
            header=self.header,
            is_test=self.is_test,
            programed_send_date=self.programed_send_date,
            sent_date=None,
            blocks=self.blocks.all(),
        )


class BlackList(models.Model):
    """
    BlackList model, if an email is in this list, it will not be sent
    """

    email = models.EmailField(unique=True)
