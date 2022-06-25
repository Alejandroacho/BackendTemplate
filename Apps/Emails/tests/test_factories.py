import pytest
from django.conf import settings
from django.db import transaction
from django.db.utils import IntegrityError
from django_rest_passwordreset.models import ResetPasswordToken
from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import SuggestionBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.factories.email import EmailFactory
from Emails.factories.email import ResetEmailFactory
from Emails.factories.email import VerifyEmailFactory
from Emails.factories.notification import NotificationFactory
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.factories.suggestion import get_subject_for_suggestion
from Emails.models.models import Block
from Emails.models.models import Email
from Emails.models.models import Notification
from Emails.models.models import Suggestion
from rest_framework.exceptions import ParseError
from Users.factories.user import UserFactory
from Users.models import User
from Users.utils import generate_user_verification_token


@pytest.mark.django_db
class TestEmailFactories:
    def test_email_factory_creates_email_with_block(self) -> None:
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        email: Email = EmailFactory(
            subject="Test subject",
            header="Test header",
        )
        assert Email.objects.count() == 1
        assert Block.objects.count() == 1
        assert email.subject == "Test subject"
        assert email.header == "Test header"
        assert email.affair is not None
        assert email.is_test is False
        assert email.to is not None
        assert email.programed_send_date is not None
        assert email.blocks is not None
        block: Block = email.blocks.first()
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is not None
        assert block.link_text is not None
        assert block.link is not None

    def test_reset_password_email_factory_raises_exception(self) -> None:
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        with pytest.raises(AttributeError):
            ResetEmailFactory()
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0

    def test_reset_password_email_factory_creates_email_with_block(
        self,
    ) -> None:
        user: User = UserFactory()
        instance: ResetPasswordToken = ResetPasswordToken.objects.create(
            user=user
        )
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        email: Email = ResetEmailFactory(instance=instance)
        assert Email.objects.count() == 1
        assert Block.objects.count() == 1
        assert email.subject == settings.RESET_PASSWORD_EMAIL_SUBJECT
        assert email.header == settings.RESET_PASSWORD_EMAIL_HEADER
        assert email.is_test is False
        assert email.affair == "SETTINGS"
        assert email.to == user
        assert email.programed_send_date is not None
        assert email.blocks is not None
        block: Block = email.blocks.first()
        assert settings.EMAIL_GREETING in block.title
        assert user.first_name in block.title
        assert block.content == settings.RESET_PASSWORD_EMAIL_CONTENT
        assert block.show_link
        assert block.link_text == settings.RESET_PASSWORD_EMAIL_LINK_TEXT
        assert settings.RESET_PASSWORD_URL in block.link

    def test_verify_email_factory_raises_exception(self) -> None:
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        with pytest.raises(IntegrityError):
            with transaction.atomic():
                VerifyEmailFactory()
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0

    def test_verify_email_factory_creates_email_with_block(self) -> None:
        user: User = UserFactory()
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        email: Email = VerifyEmailFactory(instance=user)
        assert Email.objects.count() == 1
        assert Block.objects.count() == 1
        assert email.subject == settings.VERIFY_EMAIL_SUBJECT
        assert email.header == settings.VERIFY_EMAIL_HEADER
        assert email.is_test is False
        assert email.to == user
        assert email.affair == "SETTINGS"
        assert email.programed_send_date is not None
        assert email.blocks is not None
        block: Block = email.blocks.first()
        assert settings.EMAIL_GREETING in block.title
        assert user.first_name in block.title
        assert block.content == settings.VERIFY_EMAIL_CONTENT
        assert block.show_link
        assert block.link_text == settings.VERIFY_EMAIL_LINK_TEXT
        assert settings.VERIFY_EMAIL_URL in block.link
        assert generate_user_verification_token(user) in block.link
        assert f"{user.id}" in block.link


@pytest.mark.django_db
class TestBlockFactories:
    def test_block_factory(self) -> None:
        assert Block.objects.count() == 0
        block: Block = BlockFactory()
        assert Block.objects.count() == 1
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is not None
        assert block.link_text is not None
        assert block.link is not None

    def test_reset_password_block_factory_raises_exception_without_params(
        self,
    ) -> None:
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        with pytest.raises(AttributeError):
            ResetPasswordBlockFactory()
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0

    def test_reset_password_block_factory(self) -> None:
        assert Block.objects.count() == 0
        user: User = UserFactory()
        instance: ResetPasswordToken = ResetPasswordToken.objects.create(
            user=user
        )
        block: Block = ResetPasswordBlockFactory(instance=instance)
        assert Block.objects.count() == 1
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is not None
        assert block.link_text is not None
        assert block.link is not None

    def test_verify_email_block_factory_raises_exception_without_params(
        self,
    ) -> None:
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        with pytest.raises(AttributeError):
            VerifyEmailBlockFactory()
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0

    def test_verify_email_block_factory(self) -> None:
        assert Block.objects.count() == 0
        user: User = UserFactory()
        block: Block = VerifyEmailBlockFactory(user=user)
        assert Block.objects.count() == 1
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is not None
        assert block.link_text is not None
        assert block.link is not None

    def test_suggestion_block_factory(self) -> None:
        assert Block.objects.count() == 0
        block: Block = SuggestionBlockFactory()
        assert Block.objects.count() == 1
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is False


@pytest.mark.django_db
class TestSuggestionFactory:
    def test_suggestion_email_factory_raises_exception_without_user(
        self,
    ) -> None:
        type: str = "Wrong Type"
        assert Suggestion.objects.count() == 0
        assert Block.objects.count() == 0
        with pytest.raises(ParseError):
            SuggestionEmailFactory(type=type)

    def test_suggestion_email_factory_raises_exception_due_wrong_type(
        self,
    ) -> None:
        user: User = UserFactory()
        content: str = "I found a bug"
        type: str = "wrong_suggestion_type"
        assert Suggestion.objects.count() == 0
        assert Block.objects.count() == 0
        with pytest.raises(ParseError):
            SuggestionEmailFactory(type=type, content=content, user=user)
        assert Suggestion.objects.count() == 0
        assert Block.objects.count() == 0

    def test_suggestion_email_factor_creates_email_with_block(self) -> None:
        user: User = UserFactory()
        content: str = "I found a bug"
        type: str = "ERROR"
        assert Suggestion.objects.count() == 0
        assert Block.objects.count() == 0
        suggestion: Suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        assert Suggestion.objects.count() == 1
        assert Block.objects.count() == 1
        assert suggestion.subject == "ERROR"
        assert suggestion.affair == "SUGGESTION"
        assert suggestion.header == (
            f"ERROR {settings.SUGGESTIONS_EMAIL_HEADER} {user.id}"
        )
        assert suggestion.blocks.all() is not None
        block: Block = suggestion.blocks.first()
        assert suggestion.header == block.title
        assert block.content == content
        assert block.show_link is True
        assert block.link_text == settings.SUGGESTIONS_EMAIL_LINK_TEXT
        expected_link: str = (
            f"{settings.URL}/api/suggestions/{suggestion.id}/read/"
        )
        assert block.link == expected_link

    def test_get_subject_for_suggestion_raises_an_exception(self) -> None:
        content: str = "I found a bug"
        type: str = "wrong_suggestion_type"
        with pytest.raises(ParseError):
            get_subject_for_suggestion(type, content)

    def test_get_subject_for_suggestion_returns_subject(self) -> None:
        content: str = "I found a bug"
        type: str = "ERROR"
        subject: str = get_subject_for_suggestion(type, content)
        assert subject == f"{type} || {content}"

    def test_get_subject_for_suggestion_returns_subject_without_vertical(
        self,
    ) -> None:
        content: str = "I found a bug ||"
        type: str = "ERROR"
        subject: str = get_subject_for_suggestion(type, content)
        assert subject == f"{type} || I found a bug "


@pytest.mark.django_db
class TestNotificationFactory:
    def test_notification_factory_creates_notification_with_block(
        self,
    ) -> None:
        assert Notification.objects.count() == 0
        assert Block.objects.count() == 0
        notification: Notification = NotificationFactory(
            subject="Test subject",
            header="Test header",
        )
        assert Notification.objects.count() == 1
        assert Block.objects.count() == 1
        assert notification.subject == "Test subject"
        assert notification.header == "Test header"
        assert notification.affair == "PROMOTION"
        assert notification.is_test is False
        assert notification.programed_send_date is not None
        assert notification.blocks is not None
        block: Block = notification.blocks.first()
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is not None
        assert block.link_text is not None
        assert block.link is not None

    def test_notification_factory_creates_notification_with_custom_block(
        self,
    ) -> None:
        assert Notification.objects.count() == 0
        assert Block.objects.count() == 0
        block: Block = BlockFactory()
        notification: Notification = NotificationFactory(
            subject="Test subject", header="Test header", blocks=[block]
        )
        assert Notification.objects.count() == 1
        assert Block.objects.count() == 1
        assert notification.subject == "Test subject"
        assert notification.header == "Test header"
        assert notification.affair in ["NOTIFICATION", "PROMOTION", "GENERAL"]
        assert notification.is_test is False
        assert notification.programed_send_date is not None
        assert notification.blocks is not None
        block: Block = notification.blocks.first()
        assert block.title is not None
        assert block.content is not None
        assert block.show_link is not None
        assert block.link_text is not None
        assert block.link is not None
