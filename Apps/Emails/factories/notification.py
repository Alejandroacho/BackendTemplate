from datetime import datetime

import factory
from django.db.models import Model
from django.utils import timezone
from Emails.factories.block import BlockFactory
from Emails.models.models import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = Notification

    subject: str = factory.Faker("sentence")
    header: str = factory.Faker("word")
    is_test: bool = False
    programed_send_date: datetime = timezone.now() + timezone.timedelta(
        minutes=10
    )
    sent_date: datetime = None
    was_sent: bool = False

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        if extracted:
            for block in extracted:
                self.blocks.add(block)
        else:
            self.blocks.add(BlockFactory())
