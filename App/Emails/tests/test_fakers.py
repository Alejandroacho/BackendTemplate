import pytest

from Emails.choices import CommentType
from Emails.fakers.blacklist import BlackListTestFaker
from Emails.fakers.block import BlockTestFaker
from Emails.fakers.email import EmailTestFaker
from Emails.fakers.notification import NotificationTestFaker
from Emails.fakers.suggestion import SuggestionErrorFaker
from Emails.models.models import BlackList
from Emails.models.models import Block
from Emails.models.models import Email
from Emails.models.models import Notification
from Emails.models.models import Suggestion
from Users.models import User


@pytest.mark.django_db
class TestEmailFakers:
    def test_email_faker_creates_email_with_block(self):
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        email = EmailTestFaker()
        assert Email.objects.count() == 1
        assert Block.objects.count() == 1
        assert email.subject == 'Test subject'
        assert email.header == 'Test header'
        assert email.is_test == True
        assert isinstance(email.to, User)
        assert email.blocks.first() is not None
        block = email.blocks.first()
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'


@pytest.mark.django_db
class TestBlockFakers:
    def test_block_faker_creates_block(self):
        assert Block.objects.count() == 0
        block = BlockTestFaker()
        assert Block.objects.count() == 1
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'


@pytest.mark.django_db
class TestSuggestionFakers:
    def test_suggestion_faker_creates_suggestion(self):
        assert Block.objects.count() == 0
        assert Suggestion.objects.count() == 0
        suggestion = SuggestionErrorFaker()
        assert Block.objects.count() == 1
        assert Suggestion.objects.count() == 1
        assert suggestion.subject == CommentType.SUGGESTION.value
        assert suggestion.header == 'Test header'
        assert suggestion.blocks.first() is not None
        block = suggestion.blocks.first()
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'


@pytest.mark.django_db
class TestNotificationFakers:
    def test_notification_faker_creates_notification_and_blocks(self):
        assert Block.objects.count() == 0
        assert Notification.objects.count() == 0
        notification = NotificationTestFaker()
        assert Block.objects.count() == 1
        assert Notification.objects.count() == 1
        assert notification.subject == 'Test subject'
        assert notification.header == 'Test header'
        assert notification.is_test == True
        assert notification.programed_send_date is None
        assert notification.sent_date is None
        assert notification.was_sent is False
        assert notification.blocks.first() is not None
        block = notification.blocks.first()
        assert block.title == 'test'
        assert block.content == 'test'
        assert block.show_link == True
        assert block.link_text == 'test'
        assert block.link == 'test.com'

    def test_notification_faker_creates_emails_when_send(self):
        assert Block.objects.count() == 0
        assert Email.objects.count() == 0
        assert Notification.objects.count() == 0
        notification = NotificationTestFaker(is_test=True)
        assert Block.objects.count() == 1
        assert Notification.objects.count() == 1
        notification.send()
        assert Email.objects.count() == 1


@pytest.mark.django_db
class TestBlackListFakers:
    def test_blacklist_faker_creates_blacklist(self):
        assert BlackList.objects.count() == 0
        black_list_item = BlackListTestFaker()
        assert BlackList.objects.count() == 1
        assert black_list_item.email == 'emailinblacklist@test.com'
