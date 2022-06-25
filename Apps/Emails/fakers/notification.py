from datetime import datetime

import factory
from django.db.models import Model
from Emails.factories.notification import NotificationFactory
from Emails.fakers.block import BlockTestFaker


class NotificationTestFaker(NotificationFactory):
    subject: str = "Test subject"
    header: str = "Test header"
    affair: str = "PROMOTION"
    is_test: bool = True
    programed_send_date: datetime = None
    sent_date: datetime = None
    was_sent: bool = False

    @factory.post_generation
    def blocks(self, create: bool, extracted: Model, **kwargs: dict) -> None:
        self.blocks.add(BlockTestFaker())
