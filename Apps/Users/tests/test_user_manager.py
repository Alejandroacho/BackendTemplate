import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model
from Users.models import User


@pytest.mark.django_db
class TestUsersManagers:
    def test_create_user_successfully(self) -> None:
        UserModel: Model = get_user_model()
        user: User = UserModel.objects.create_user(
            email="normaluser@test.com",
            first_name="test_name",
            last_name="test_last_name",
            password="test_password",
        )
        assert user.email == "normaluser@test.com"
        assert user.is_active == True
        assert user.username == None

    def test_create_user_fails_without_data(self) -> None:
        UserModel: Model = get_user_model()
        with pytest.raises(TypeError):
            UserModel.objects.create_user()

    def test_create_user_fails_with_email_and_without_password(self) -> None:
        UserModel: Model = get_user_model()
        with pytest.raises(TypeError):
            UserModel.objects.create_user(email="email@test.com", password="")

    def test_create_user_fails_without_email_with_all_data(self) -> None:
        UserModel: Model = get_user_model()
        with pytest.raises(ValueError):
            UserModel.objects.create_user(
                email=None,
                first_name="test_name",
                last_name="test_last_name",
                password="test_password",
            )

    def test_create_superuser(self) -> None:
        UserModel: Model = get_user_model()
        admin_user: User = UserModel.objects.create_superuser(
            email="super@user.com",
            first_name="test_name",
            last_name="test_last_name",
            password="test_password",
        )
        assert admin_user.email == "super@user.com"
        assert admin_user.is_verified == True
        assert admin_user.username == None

    def test_create_superuser_fails_without_data(self) -> None:
        UserModel: Model = get_user_model()
        with pytest.raises(TypeError):
            UserModel.objects.create_superuser()

    def test_create_superuser_fails_with_email_and_without_password(
        self,
    ) -> None:
        UserModel: Model = get_user_model()
        with pytest.raises(TypeError):
            UserModel.objects.create_superuser(
                email="adminemail@test.com", password=""
            )

    def test_create_superuser_fails_with_email_without_password(self) -> None:
        UserModel: Model = get_user_model()
        with pytest.raises(TypeError):
            UserModel.objects.create_superuser(email="", password="foo")
