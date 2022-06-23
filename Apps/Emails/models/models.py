from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignObject
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

    title: Field = models.CharField(max_length=100, null=True)
    content: Field = models.TextField(null=True)
    show_link: Field = models.BooleanField(default=False)
    link_text: Field = models.CharField(max_length=100, null=True)
    link: Field = models.URLField(max_length=100, null=True)

    def __str__(self) -> str:
        return f"{self.id} | {self.title}"


class Email(AbstractEmailClass):
    """
    Email model
    """

    subject: Field = models.CharField(max_length=100)
    is_test: Field = models.BooleanField(default=False)
    programed_send_date: Field = models.DateTimeField(null=True)
    to: ForeignObject = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="to_user"
    )

    def get_emails(self) -> list:
        return [self.to.email]

    def set_programed_send_date(self) -> None:
        programmed_date: datetime = self.programed_send_date
        if programmed_date and programmed_date <= timezone.now():
            message: str = "Programed send date must be future"
            raise ValidationError(message, code="invalid")
        if not programmed_date:
            five_minutes_ahead: datetime = timezone.now() + timezone.timedelta(
                minutes=5
            )
            self.programed_send_date = five_minutes_ahead

    def save(self, *args: tuple, **kwargs: dict) -> None:
        if self.is_test:
            self.to = EmailTestUserFaker()
        self.set_programed_send_date()
        super(Email, self).save(*args, **kwargs)


class Suggestion(AbstractEmailClass):
    """
    Suggestion model, emails that will be sent to admin suggestions email
    """

    user: ForeignObject = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="suggestion", unique=False
    )
    subject: Field = models.CharField(
        max_length=100,
        choices=CommentType.choices,
        default=CommentType.SUGGESTION.value,
    )
    was_read: Field = models.BooleanField(default=False)

    def get_emails(self) -> list:
        return [settings.SUGGESTIONS_EMAIL]


class Notification(AbstractEmailClass):
    """
    Notification model, it creates an email for each user with this data
    """

    subject: Field = models.CharField(max_length=100)
    is_test: Field = models.BooleanField(default=False)
    programed_send_date: Field = models.DateTimeField(null=True)

    def send(self) -> None:
        if self.is_test:
            self.create_email(to=EmailTestUserFaker())
        else:
            for user in User.objects.all():
                self.create_email(user)
        self.sent_date: datetime = timezone.now()
        self.was_sent: bool = True
        self.save()

    def create_email(self, to: User) -> None:
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

    email: Field = models.EmailField(unique=True)
