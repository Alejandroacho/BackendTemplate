import factory
from django.conf import settings

from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    phone_number = factory.Faker('msisdn')


class VerifiedUserFaker(UserFaker):
    phone_number = factory.Faker('msisdn')
    is_verified = True


class AdminFaker(UserFactory):
    phone_number = factory.Faker('msisdn')
    is_admin = True
    is_verified = True


class EmailTestUserFaker(UserFactory):
    phone_number = '+34123456789'
    is_verified = True
    email = settings.TEST_EMAIL
