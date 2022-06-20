from datetime import datetime

import factory
import factory.fuzzy
from django.db.models import ImageField
from django.db.models import Model

from Users.factories.user import UserFactory
from Users.models import Profile
from Users.models import User


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = Profile

    user: User = factory.SubFactory(UserFactory)
    nickname: str = factory.Faker("isbn13")
    bio: str = factory.Faker("text")
    image: ImageField = factory.django.ImageField(
        filename="profile_picture.jpg",
        width=100,
        height=100,
        format="JPEG",
        color="gray",
    )
    gender: str = factory.fuzzy.FuzzyChoice(("F", "M", "N", "P"))
    birth_date: datetime = factory.Faker("date")
