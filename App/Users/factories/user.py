import factory

from Users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', 'phone_number')

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_admin = False
    is_verified = False
    phone_number = factory.Faker('msisdn')

    @factory.post_generation
    def set_phone_number(self, create, extracted, **kwargs):
        has_extension = str(self.phone_number)[0] == '+'
        if create and not has_extension:
            self.phone_number = f'+1{self.phone_number}'
            self.save()
