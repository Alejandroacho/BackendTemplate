import factory
import factory.fuzzy
from django.db.models import Model
from Emails.models.models import BlackList
from Emails.models.models import Email
from Users.factories.user import UserFactory
from Users.models import User


class BlackListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = BlackList

    user: User = factory.SubFactory(UserFactory)
    affairs: str = factory.fuzzy.FuzzyChoice(
        (
            "NOTIFICATION",
            "PROMOTION",
            "GENERAL",
            "SETTINGS",
            "INVOICE",
            "SUGGESTION"
        )
    )
