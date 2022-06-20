import pytest

from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory
from Users.models import Profile
from Users.models import User


@pytest.mark.django_db
class TestUserFactory:
    def test_user_factory(self):
        assert User.objects.count() == 0
        user = UserFactory()
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email is not None
        assert user.phone_number is not None
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is False
        assert user.is_verified is False


@pytest.mark.django_db
class TestProfileFactory:
    def test_profile_factory(self):
        assert Profile.objects.count() == 0
        profile = ProfileFactory()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio is not None
        assert profile.gender is not None
        assert profile.birth_date is not None
        assert profile.image is not None
        assert profile.image.url is not None
