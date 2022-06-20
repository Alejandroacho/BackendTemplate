import factory
from django.db.models import Model

from Emails.models.models import BlackList
from Emails.models.models import Email


class BlackListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = BlackList

    email: Email = factory.Faker("email")
