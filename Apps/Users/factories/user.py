import factory
from django.db.models import Model

from Users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model: Model = User
        django_get_or_create: tuple = ("email", "phone_number")

    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    email: str = factory.Faker("email")
    password: str = factory.PostGenerationMethodCall(
        "set_password", "password"
    )
    is_admin: bool = False
    is_verified: bool = False
    phone_number: str = factory.Faker("msisdn")

    @factory.post_generation
    def set_phone_number(
        self, create: bool, extracted: Model, **kwargs: dict
    ) -> None:
        has_extension: bool = str(self.phone_number)[0] == "+"
        if create and not has_extension:
            self.phone_number = f"+1{self.phone_number}"
            self.save()
