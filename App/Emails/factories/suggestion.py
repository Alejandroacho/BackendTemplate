import factory
from django.conf import settings
from rest_framework.exceptions import ParseError

from Emails.choices import CommentType
from Emails.factories.block import SuggestionBlockFactory
from Emails.models.models import Suggestion


class SuggestionEmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Suggestion

    class Params:
        type = ''
        content = ''

    subject = factory.LazyAttribute(
        lambda object: get_subject_for_suggestion(object.type, object.content)
    )

    @factory.post_generation
    def header(self, create, extracted, **kwargs):
        self.header = (
            f'{self.subject.split("||")[0][:-1]}'
            + f' {settings.SUGGESTIONS_EMAIL_HEADER}'
            + f' {self.user.id}'
        )

    @factory.post_generation
    def blocks(self, create, extracted, **kwargs):
        subject_splitted = self.subject.split('||')
        type = subject_splitted[0][:-1]
        content = subject_splitted[1][1:]
        self.subject = type
        self.save()
        block = SuggestionBlockFactory(
            title=self.header,
            content=content,
            show_link=True,
            link_text=settings.SUGGESTIONS_EMAIL_LINK_TEXT,
            link=f'{settings.URL}/api/suggestions/{self.id}/read/',
        )
        self.blocks.add(block)


def get_subject_for_suggestion(suggestion_type, content):
    if suggestion_type not in CommentType.values:
        raise ParseError('Type not allowed')
    return f'{suggestion_type} || {content.replace("||", "")}'
