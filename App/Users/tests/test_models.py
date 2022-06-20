import pytest

from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory
from Users.fakers.profile import AdultProfileFaker
from Users.fakers.profile import KidProfileFaker
from Users.fakers.user import AdminFaker
from Users.utils import generate_user_verification_token


@pytest.mark.django_db
class TestUserModel:
    def test_model_has_attributes(self):
        user = UserFactory()
        assert hasattr(user, 'email')
        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')
        assert hasattr(user, 'password')
        assert hasattr(user, 'is_verified')
        assert hasattr(user, 'is_premium')
        assert hasattr(user, 'is_admin')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')

    def test_model_do_not_has_attributes(self):
        user = UserFactory()
        assert user.username == None
        assert user.is_superuser == None
        assert user.last_login == None

    def test_model_has_custom_properties(self):
        user = UserFactory()
        assert user.name == user.first_name + ' ' + user.last_name
        assert user.is_staff == user.is_admin

    def test_model_verify_function(self):
        user = UserFactory()
        assert user.is_verified == False
        user.verify()
        assert user.is_verified == True

    def test_has_permission_returns_false(self):
        user = UserFactory()
        user2 = UserFactory()
        has_permission = user.has_permission(user2)
        assert has_permission == False

    def test_has_permission_returns_true(self):
        user = UserFactory()
        has_permission = user.has_permission(user)
        assert has_permission == True

    def test_has_module_perms_as_admin(self):
        user = AdminFaker()
        assert user.has_module_perms('Users') == True
        assert user.has_module_perms('Emails') == True
        assert user.has_module_perms('Logs') == True

    def test_has_module_perms_as_not_admin(self):
        user = UserFactory()
        assert user.has_module_perms('Users') == False
        assert user.has_module_perms('Emails') == False
        assert user.has_module_perms('Logs') == False

    def test_str_user(self):
        user = UserFactory()
        assert str(user) == f'{user.email}'


@pytest.mark.django_db
class TestProfileModel:
    def test_model_has_attributes(self):
        profile = ProfileFactory()
        dict_keys = profile.__dict__.keys()
        attributes = [attribute for attribute in dict_keys]
        assert 'user_id' in attributes
        assert 'nickname' in attributes
        assert 'bio' in attributes
        assert 'image' in attributes
        assert 'gender' in attributes
        assert 'preferred_language' in attributes
        assert 'birth_date' in attributes
        assert 'created_at' in attributes
        assert 'updated_at' in attributes

    def test_profile_str(self):
        profile = ProfileFactory()
        expected_str = f'User ({profile.user_id}) profile ({profile.pk})'
        assert str(profile) == expected_str

    def test_is_adult(self):
        adult_profile = AdultProfileFaker()
        expected_result = True
        assert adult_profile.is_adult() == expected_result

    def test_is_not_adult(self):
        kid_profile = KidProfileFaker()
        expected_result = False
        assert kid_profile.is_adult() == expected_result

    def test_is_adult_without_birth_date(self):
        profile = ProfileFactory(birth_date=None)
        expected_result = None
        assert profile.is_adult() == expected_result
