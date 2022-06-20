import pytest

from Users.fakers.profile import AdultProfileFaker
from Users.fakers.profile import FemaleProfileFaker
from Users.fakers.profile import KidProfileFaker
from Users.fakers.profile import MaleProfileFaker
from Users.fakers.profile import NonBinaryProfileFaker
from Users.fakers.profile import NotSaidProfileFaker
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User


@pytest.mark.django_db
class TestUserFakers:
    def test_user_faker(self):
        assert User.objects.count() == 0
        user = UserFaker(
            email='normaluser@appname.me', phone_number='+1123123123'
        )
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == 'normaluser@appname.me'
        assert str(user.phone_number) == '+1123123123'
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is False
        assert user.is_verified is False

    def test_verified_user_faker(self):
        assert User.objects.count() == 0
        user = VerifiedUserFaker(email='normalverifieduser@appname.me')
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == 'normalverifieduser@appname.me'
        assert str(user.phone_number)[0] == '+'
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is False
        assert user.is_verified is True

    def test_admin_user_faker(self):
        assert User.objects.count() == 0
        user = AdminFaker(
            email='adminuser@appname.me', phone_number='+1123123124'
        )
        assert User.objects.count() == 1
        assert user.name is not None
        assert user.email == 'adminuser@appname.me'
        assert str(user.phone_number) == '+1123123124'
        assert user.password is not None
        assert user.check_password('password') is True
        assert user.is_admin is True
        assert user.is_verified is True


@pytest.mark.django_db
class TestProfileFakers:
    def test_adult_profile_faker(self):
        assert Profile.objects.count() == 0
        profile = AdultProfileFaker()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio == 'Custom bio for adult profile'
        assert profile.gender is not None
        assert profile.birth_date is not None
        assert profile.is_adult() is True
        assert profile.image is not None
        assert profile.image.url is not None

    def test_kid_profile_faker(self):
        assert Profile.objects.count() == 0
        profile = KidProfileFaker()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio == 'Custom bio for kid profile'
        assert profile.gender is not None
        assert profile.birth_date is not None
        assert profile.is_adult() is False
        assert profile.image is not None
        assert profile.image.url is not None

    def test_female_profile_faker(self):
        assert Profile.objects.count() == 0
        profile = FemaleProfileFaker()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio == 'Custom bio for female profile'
        assert profile.gender is not None
        assert profile.gender == 'F'
        assert profile.birth_date is not None
        assert profile.image is not None
        assert profile.image.url is not None

    def test_male_profile_faker(self):
        assert Profile.objects.count() == 0
        profile = MaleProfileFaker()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio == 'Custom bio for male profile'
        assert profile.gender is not None
        assert profile.gender == 'M'
        assert profile.birth_date is not None
        assert profile.image is not None
        assert profile.image.url is not None

    def test_non_binary_profile_faker(self):
        assert Profile.objects.count() == 0
        profile = NonBinaryProfileFaker()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio == 'Custom bio for non-binary profile'
        assert profile.gender is not None
        assert profile.gender == 'N'
        assert profile.birth_date is not None
        assert profile.image is not None
        assert profile.image.url is not None

    def test_not_said_profile_faker(self):
        assert Profile.objects.count() == 0
        profile = NotSaidProfileFaker()
        assert Profile.objects.count() == 1
        assert profile.user is not None
        assert profile.nickname is not None
        assert profile.bio == 'Custom bio for x profile'
        assert profile.gender is not None
        assert profile.gender == 'P'
        assert profile.birth_date is not None
        assert profile.image is not None
        assert profile.image.url is not None
