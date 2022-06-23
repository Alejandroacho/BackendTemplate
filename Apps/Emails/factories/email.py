from datetime import datetime

import factory
from django.conf import settings
from django.db.models import Model
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken
from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.models.models import Block
from Emails.models.models import Email
from Users.factories.user import UserFactory
from Users.models import User


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = Email

    subject: str = factory.Faker("sentence")
    header: str = factory.Faker("word")
    is_test: bool = False
    to: User = factory.SubFactory(UserFactory)
    programed_send_date: datetime = timezone.now() + timezone.timedelta(
        minutes=10
    )
    sent_date: datetime = factory.Faker(
        "date_time", tzinfo=timezone.get_current_timezone()
    )
    was_sent: bool = False

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if not create:
            return
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())


class ResetEmailFactory(EmailFactory):
    class Params:
        instance: ResetPasswordToken = None

    subject: str = settings.RESET_PASSWORD_EMAIL_SUBJECT
    header: str = settings.RESET_PASSWORD_EMAIL_HEADER
    to: User = factory.LazyAttribute(lambda object: object.instance.user)
    programed_send_date: datetime = None

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        token: ResetPasswordToken = ResetPasswordToken.objects.filter(
            user_id=self.to.id
        ).last()
        block: Block = ResetPasswordBlockFactory(instance=token)
        self.blocks.add(block)


class VerifyEmailFactory(EmailFactory):
    class Params:
        instance: User = None

    subject: str = settings.VERIFY_EMAIL_SUBJECT
    header: str = settings.VERIFY_EMAIL_HEADER
    to: User = factory.LazyAttribute(lambda object: object.instance)
    programed_send_date: datetime = None

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        block: Block = VerifyEmailBlockFactory(user=self.to)
        self.blocks.add(block)
