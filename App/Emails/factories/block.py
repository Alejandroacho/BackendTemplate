import factory
from django.conf import settings
from django.db.models import Model

from Emails.models.models import Block
from Users.models import User
from Users.utils import generate_user_verification_token


class BlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = Block

    title: str = factory.Faker("word")
    content: str = factory.Faker("sentence")
    show_link: bool = factory.Faker("boolean")
    link_text: str = factory.Faker("word")
    link: str = factory.Faker("url")


class ResetPasswordBlockFactory(BlockFactory):
    class Params:
        instance: User = None

    title: str = factory.LazyAttribute(
        lambda object: (
            f"{settings.EMAIL_GREETING}" f" {object.instance.user.first_name}!"
        )
    )
    content: str = settings.RESET_PASSWORD_EMAIL_CONTENT
    show_link: bool = True
    link_text: str = settings.RESET_PASSWORD_EMAIL_LINK_TEXT
    link: str = factory.LazyAttribute(
        lambda object: f"{settings.RESET_PASSWORD_URL}/{object.instance.key}"
    )


class VerifyEmailBlockFactory(BlockFactory):
    class Params:
        user: User = None

    title: str = factory.LazyAttribute(
        lambda object: (
            f"{settings.EMAIL_GREETING}" f"{object.user.first_name}!"
        )
    )
    content: str = settings.VERIFY_EMAIL_CONTENT
    show_link: bool = True
    link_text: str = settings.VERIFY_EMAIL_LINK_TEXT
    link: str = factory.LazyAttribute(
        lambda object: (
            f"{settings.VERIFY_EMAIL_URL}/{object.user.id}/verify/?token="
            f"{generate_user_verification_token(object.user)}"
        )
    )


class SuggestionBlockFactory(BlockFactory):
    show_link: bool = False
    link_text: str = ""
    link: str = ""
