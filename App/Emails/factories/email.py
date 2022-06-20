import factory
from django.conf import settings
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken

from Emails.factories.block import BlockFactory
from Emails.factories.block import ResetPasswordBlockFactory
from Emails.factories.block import VerifyEmailBlockFactory
from Emails.models.models import Email
from Users.factories.user import UserFactory


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Email

    subject = factory.Faker('sentence')
    header = factory.Faker('word')
    is_test = False
    to = factory.SubFactory(UserFactory)
    programed_send_date = timezone.now() + timezone.timedelta(minutes=10)
    sent_date = factory.Faker(
        'date_time', tzinfo=timezone.get_current_timezone()
    )
    was_sent = False

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())


class ResetEmailFactory(EmailFactory):
    class Params:
        instance = None

    subject = settings.RESET_PASSWORD_EMAIL_SUBJECT
    header = settings.RESET_PASSWORD_EMAIL_HEADER
    to = factory.LazyAttribute(lambda object: object.instance.user)
    programed_send_date = None

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        token = ResetPasswordToken.objects.filter(user_id=self.to.id).last()
        block = ResetPasswordBlockFactory(instance=token)
        self.blocks.add(block)


class VerifyEmailFactory(EmailFactory):
    class Params:
        instance = None

    subject = settings.VERIFY_EMAIL_SUBJECT
    header = settings.VERIFY_EMAIL_HEADER
    to = factory.LazyAttribute(lambda object: object.instance)
    programed_send_date = None

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        block = VerifyEmailBlockFactory(user=self.to)
        self.blocks.add(block)
