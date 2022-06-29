from datetime import datetime

import pytest
from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from Emails.factories.blacklist import BlackListFactory
from Emails.factories.block import BlockFactory
from Emails.factories.email import EmailFactory
from Emails.factories.notification import NotificationFactory
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.fakers.suggestion import SuggestionErrorFaker
from Emails.models.abstracts import AbstractEmailClass
from Emails.models.models import BlackList
from Emails.models.models import Block
from Emails.models.models import Email
from Emails.models.models import Notification
from Emails.models.models import Suggestion
from Users.fakers.user import EmailTestUserFaker
from Users.fakers.user import UserFaker
from Users.models import User


@pytest.mark.django_db
class TestBlockModel:
    def test_block_attributes(self) -> None:
        block: Block = BlockFactory()
        dict_keys: dict = block.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "title" in attributes
        assert "content" in attributes
        assert "show_link" in attributes
        assert "link_text" in attributes
        assert "link" in attributes

    def test_block_str(self) -> None:
        block: Block = BlockFactory()
        expected_str: str = f"{block.id} | {block.title}"
        assert str(block) == expected_str


@pytest.mark.django_db
class TestEmailModel:
    def test_get_emails_abstract_class_fails(self) -> None:
        abstract: AbstractEmailClass = AbstractEmailClass()
        with pytest.raises(ValueError):
            abstract.get_email()

    def test_email_attributes(self) -> None:
        email: Email = EmailFactory()
        dict_keys: dict = email.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "subject" in attributes
        assert "header" in attributes
        assert "is_test" in attributes
        assert "to_id" in attributes
        assert "programed_send_date" in attributes
        assert "sent_date" in attributes
        assert "was_sent" in attributes

    def test_email_str(self) -> None:
        email: Email = EmailFactory()
        expected_str: str = f"{email.id} | {email.subject}"
        assert str(email) == expected_str

    def test_save(self) -> None:
        user: User = UserFaker()
        email: Email = EmailFactory.build()
        email.programed_send_date = None
        email.to = user
        email.is_test = False
        assert email.programed_send_date is None
        assert email.to == user
        assert email.is_test is False
        email.save()
        assert email.programed_send_date is not None
        assert email.to == user

    def test_saving_an_email_without_date(self) -> None:
        user: User = UserFaker()
        email: Email = EmailFactory.build()
        email.programed_send_date = None
        email.to = user
        email.is_test = False
        assert email.programed_send_date is None
        assert email.is_test is False
        email.save()
        assert email.programed_send_date is not None

    def test_saving_fails_with_wrong_programed_date(self) -> None:
        now: datetime = timezone.now()
        one_year_before: datetime = now - timezone.timedelta(days=365)
        with pytest.raises(ValidationError):
            user = EmailTestUserFaker()
            EmailFactory(to=user, programed_send_date=one_year_before)

    def test_saving_an_email_with_emails(self) -> None:
        user: User = UserFaker()
        email: Email = EmailFactory.build()
        email.to = user
        email.is_test = False
        assert email.to == user
        assert email.is_test is False
        email.save()
        assert email.to == user

    def test_saving_an_email_with_emails_as_test(self) -> None:
        user: User = UserFaker()
        email: Email = EmailFactory.build()
        email.to = user
        email.is_test = True
        assert email.to == user
        assert email.is_test is True
        email.save()
        assert email.to == EmailTestUserFaker()

    def test_get_emails_with_emails_as_test(self) -> None:
        user: User = UserFaker()
        email: Email = EmailFactory(to=user, is_test=True)
        assert email.to == EmailTestUserFaker()
        assert user != EmailTestUserFaker()

    def test_get_emails_data_with_blocks(self) -> None:
        block: Block = BlockFactory()
        email: Email = EmailFactory(blocks=[block])
        data: dict = email.get_email_data()
        assert data["header"] == email.header
        assert list(data["blocks"]) == list(email.blocks.all())

    def test_get_emails_data_without_blocks(self) -> None:
        email: Email = EmailFactory(blocks=None)
        email.blocks.all().delete()
        data: dict = email.get_email_data()
        assert data["header"] == email.header
        assert data["blocks"] == []

    def test_get_template(self) -> None:
        email: Email = EmailFactory()
        data: dict = email.get_email_data()
        template: str = email.get_template()
        expected_template: str = render_to_string("email.html", data)
        assert template == expected_template

    def test_get_email_object(self) -> None:
        email: Email = EmailFactory()
        email_object: EmailMultiAlternatives = email.get_email_object()
        assert isinstance(email_object, EmailMultiAlternatives)

    def test_send_email(self) -> None:
        assert len(mail.outbox) == 0
        email: Email = EmailFactory()
        email.send()
        assert email.was_sent is True
        assert len(mail.outbox) == 1

    def test_send_email_fails_because_is_in_blacklist(self) -> None:
        assert len(mail.outbox) == 0
        email: Email = EmailFactory(affair="GENERAL")
        BlackListFactory(user=email.to, affairs="GENERAL")
        email.send()
        assert email.was_sent is False
        assert len(mail.outbox) == 0


@pytest.mark.django_db
class TestSuggestionModel:
    """
    As all the functions are an abstract class inherit in the Email model, we
    only test the attributes of this model, as all the functions are tested
    """

    def test_email_attributes(self) -> None:
        type: str = "ERROR"
        user: User = UserFaker()
        content: str = "This is the content"
        email: Email = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        dict_keys: dict = email.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "user_id" in attributes
        assert "subject" in attributes
        assert "header" in attributes
        assert "is_test" not in attributes
        assert "programed_send_date" not in attributes
        assert "sent_date" in attributes
        assert "was_sent" in attributes
        assert "was_read" in attributes

    def test_get_emails(self) -> None:
        email: Suggestion = SuggestionErrorFaker()
        assert email.get_email() == settings.SUGGESTIONS_EMAIL

    def test_send_suggestion(self) -> None:
        assert len(mail.outbox) == 0
        email: Suggestion = SuggestionErrorFaker()
        email.send()
        assert len(mail.outbox) == 1


@pytest.mark.django_db
class TestNotificationModel:
    def test_notification_attributes(self) -> None:
        notification: Notification = NotificationFactory()
        dict_keys: dict = notification.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "subject" in attributes
        assert "header" in attributes
        assert "is_test" in attributes
        assert "programed_send_date" in attributes
        assert "sent_date" in attributes
        assert "was_sent" in attributes

    def test_send_notification_with_is_test_attribute_as_true(self) -> None:
        assert Email.objects.all().count() == 0
        notification: Notification = NotificationFactory(is_test=True)
        assert notification.sent_date is None
        assert notification.was_sent is False
        notification.send()
        assert Email.objects.all().count() == 1
        assert Email.objects.first().to == EmailTestUserFaker()
        assert notification.sent_date is not None
        assert notification.was_sent is True

    def test_send_notification_with_is_test_attribute_as_false(self) -> None:
        assert Email.objects.all().count() == 0
        first_user: User = UserFaker()
        second_user: User = UserFaker()
        notification: Notification = NotificationFactory(is_test=False)
        assert notification.sent_date is None
        assert notification.was_sent is False
        notification.send()
        assert Email.objects.all().count() == 2
        assert Email.objects.first().to == first_user
        assert Email.objects.last().to == second_user
        assert notification.sent_date is not None
        assert notification.was_sent is True

    def test_create_email(self) -> None:
        notification: Notification = NotificationFactory()
        user: User = UserFaker()
        assert Email.objects.all().count() == 0
        notification.create_email(to=user)
        assert Email.objects.all().count() == 1
        assert Email.objects.first().to == user
        assert Email.objects.first().subject == notification.subject
        assert Email.objects.first().header == notification.header
        assert Email.objects.first().is_test is False
        assert (
            Email.objects.first().programed_send_date
            == notification.programed_send_date
        )
        assert (
            Email.objects.first().blocks.all()[0].id
            == notification.blocks.all()[0].id
        )


@pytest.mark.django_db
class TestBlackListModel:
    def test_black_list_item_attributes(self) -> None:
        black_list_item: BlackList = BlackListFactory()
        dict_keys: dict = black_list_item.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "user_id" in attributes
        assert "affairs" in attributes
