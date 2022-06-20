from datetime import datetime

import factory
from dateutil.relativedelta import relativedelta

from Users.factories.profile import ProfileFactory


class FemaleProfileFaker(ProfileFactory):
    nickname = factory.Faker('name_female')
    bio = 'Custom bio for female profile'
    gender = 'F'


class MaleProfileFaker(ProfileFactory):
    nickname = factory.Faker('name_male')
    bio = 'Custom bio for male profile'
    gender = 'M'


class NonBinaryProfileFaker(ProfileFactory):
    nickname = factory.Faker('name_nonbinary')
    bio = 'Custom bio for non-binary profile'
    gender = 'N'


class NotSaidProfileFaker(ProfileFactory):
    nickname = factory.Faker('suffix')
    bio = 'Custom bio for x profile'
    gender = 'P'


class AdultProfileFaker(ProfileFactory):
    bio = 'Custom bio for adult profile'
    birth_date = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=20)).strftime('%Y-%m-%d')
        )
    )


class KidProfileFaker(ProfileFactory):
    bio = 'Custom bio for kid profile'
    birth_date = factory.LazyAttribute(
        lambda object: (
            (datetime.now() - relativedelta(years=15)).strftime('%Y-%m-%d')
        )
    )
