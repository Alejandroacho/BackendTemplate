import factory

from Emails.models.models import BlackList


class BlackListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlackList

    email = factory.Faker('email')
