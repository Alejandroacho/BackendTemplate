from datetime import datetime

import factory
from dateutil.relativedelta import relativedelta

from Users.factories.profile import ProfileFactory


class FemaleProfileFaker(ProfileFactory):
    nickname: str = factory.Faker("name_female")
    bio: str = "Custom bio for female profile"
    gender: str = "F"


class MaleProfileFaker(ProfileFactory):
    nickname: str = factory.Faker("name_male")
    bio: str = "Custom bio for male profile"
    gender: str = "M"


class NonBinaryProfileFaker(ProfileFactory):
    nickname: str = factory.Faker("name_nonbinary")
    bio: str = "Custom bio for non-binary profile"
    gender: str = "N"


class NotSaidProfileFaker(ProfileFactory):
    nickname: str = factory.Faker("suffix")
    bio: str = "Custom bio for x profile"
    gender: str = "P"


class AdultProfileFaker(ProfileFactory):
    bio: str = "Custom bio for adult profile"
    birth_date: datetime = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=20)).strftime("%Y-%m-%d")
        )
    )


class KidProfileFaker(ProfileFactory):
    bio: str = "Custom bio for kid profile"
    birth_date: datetime = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=15)).strftime("%Y-%m-%d")
        )
    )
