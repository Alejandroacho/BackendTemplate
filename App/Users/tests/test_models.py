import pytest

from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory
from Users.fakers.profile import AdultProfileFaker
from Users.fakers.profile import KidProfileFaker
from Users.fakers.user import AdminFaker
from Users.models import Profile
from Users.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_model_has_attributes(self) -> None:
        user: User = UserFactory()
        assert hasattr(user, "email")
        assert hasattr(user, "first_name")
        assert hasattr(user, "last_name")
        assert hasattr(user, "password")
        assert hasattr(user, "is_verified")
        assert hasattr(user, "is_premium")
        assert hasattr(user, "is_admin")
        assert hasattr(user, "created_at")
        assert hasattr(user, "updated_at")

    def test_model_do_not_has_attributes(self) -> None:
        user: User = UserFactory()
        assert user.username == None
        assert user.is_superuser == None
        assert user.last_login == None

    def test_model_has_custom_properties(self) -> None:
        user: User = UserFactory()
        assert user.name == user.first_name + " " + user.last_name
        assert user.is_staff == user.is_admin

    def test_model_verify_function(self) -> None:
        user: User = UserFactory()
        assert user.is_verified == False
        user.verify()
        assert user.is_verified == True

    def test_has_permission_returns_false(self) -> None:
        user: User = UserFactory()
        user2: User = UserFactory()
        has_permission: bool = user.has_permission(user2)
        assert has_permission == False

    def test_has_permission_returns_true(self) -> None:
        user: User = UserFactory()
        has_permission: bool = user.has_permission(user)
        assert has_permission == True

    def test_has_module_perms_as_admin(self) -> None:
        user: User = AdminFaker()
        assert user.has_module_perms("Users") == True
        assert user.has_module_perms("Emails") == True
        assert user.has_module_perms("Logs") == True

    def test_has_module_perms_as_not_admin(self) -> None:
        user: User = UserFactory()
        assert user.has_module_perms("Users") == False
        assert user.has_module_perms("Emails") == False
        assert user.has_module_perms("Logs") == False

    def test_str_user(self) -> None:
        user: User = UserFactory()
        assert str(user) == f"{user.email}"


@pytest.mark.django_db
class TestProfileModel:
    def test_model_has_attributes(self) -> None:
        profile: Profile = ProfileFactory()
        dict_keys: dict = profile.__dict__.keys()
        attributes: list = [attribute for attribute in dict_keys]
        assert "user_id" in attributes
        assert "nickname" in attributes
        assert "bio" in attributes
        assert "image" in attributes
        assert "gender" in attributes
        assert "preferred_language" in attributes
        assert "birth_date" in attributes
        assert "created_at" in attributes
        assert "updated_at" in attributes

    def test_profile_str(self) -> None:
        profile: Profile = ProfileFactory()
        expected_str: str = f"User ({profile.user_id}) profile ({profile.pk})"
        assert str(profile) == expected_str

    def test_is_adult(self) -> None:
        adult_profile: Profile = AdultProfileFaker()
        expected_result: bool = True
        assert adult_profile.is_adult() == expected_result

    def test_is_not_adult(self) -> None:
        kid_profile: Profile = KidProfileFaker()
        expected_result: bool = False
        assert kid_profile.is_adult() == expected_result

    def test_is_adult_without_birth_date(self) -> None:
        profile: Profile = ProfileFactory(birth_date=None)
        expected_result: None = None
        assert profile.is_adult() == expected_result
