import factory

from Emails.factories.notification import NotificationFactory
from Emails.fakers.block import BlockTestFaker


class NotificationTestFaker(NotificationFactory):
    subject = 'Test subject'
    header = 'Test header'
    is_test = True
    programed_send_date = None
    sent_date = None
    was_sent = False

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        self.blocks.add(BlockTestFaker())
