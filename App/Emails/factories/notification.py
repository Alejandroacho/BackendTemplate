import factory
from django.utils import timezone

from Emails.factories.block import BlockFactory
from Emails.models.models import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    subject = factory.Faker('sentence')
    header = factory.Faker('word')
    is_test = False
    programed_send_date = timezone.now() + timezone.timedelta(minutes=10)
    sent_date = None
    was_sent = False

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())
