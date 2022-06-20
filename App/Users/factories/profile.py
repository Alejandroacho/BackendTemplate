import factory
import factory.fuzzy

from Users.factories.user import UserFactory
from Users.models import Profile


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    nickname = factory.Faker('isbn13')
    bio = factory.Faker('text')
    image = factory.django.ImageField(
        filename='profile_picture.jpg',
        width=100,
        height=100,
        format='JPEG',
        color='gray',
    )
    gender = factory.fuzzy.FuzzyChoice(('F', 'M', 'N', 'P'))
    birth_date = factory.Faker('date')
