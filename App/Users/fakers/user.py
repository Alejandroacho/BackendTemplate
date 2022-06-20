import factory
from django.conf import settings

from Users.factories.user import UserFactory


class UserFaker(UserFactory):
    phone_number: str = factory.Faker("msisdn")


class VerifiedUserFaker(UserFaker):
    phone_number: str = factory.Faker("msisdn")
    is_verified: bool = True


class AdminFaker(UserFactory):
    phone_number: str = factory.Faker("msisdn")
    is_admin: bool = True
    is_verified: bool = True


class EmailTestUserFaker(UserFactory):
    phone_number: str = "+34123456789"
    is_verified: bool = True
    email: str = settings.TEST_EMAIL
