import json

import pytest
from django.core import mail
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.response import Response
from rest_framework.test import APIClient

from Users.factories.user import UserFactory
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User
from Users.utils import generate_user_verification_token


ENDPOINT: str = "/api/users"


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUserSignUpEndpoint:
    def test_create_user_fails_with_an_used_email(
        self, client: APIClient
    ) -> None:
        UserFactory(email="emailused@appname.me")
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailused@appname.me",
            "password": "password",
            "password_confirmation": "password",
        }
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
        message_one: str = "email"
        message_two: str = "This field must be unique"
        assert response.status_code == 400
        assert message_one in response.data
        assert message_two in response.data["email"][0]
        assert len(mail.outbox) == 0

    def test_create_user_fails_with_a_common_password(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemail@appname.me",
            "password": "password",
            "password_confirmation": "password",
        }
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
        message: str = "This password is too common."
        assert response.status_code == 400
        assert message in response.data["non_field_errors"][0]
        assert len(mail.outbox) == 0

    def test_create_user_is_successfull(self, client: APIClient) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemail@appname.me",
            "password": "strongpassword",
            "password_confirmation": "strongpassword",
        }
        assert User.objects.count() == 0
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert response.data["first_name"] == data["first_name"]
        assert response.data["last_name"] == data["last_name"]
        assert response.data["email"] == data["email"]
        assert response.data["phone_number"] == None
        assert response.data["is_verified"] == False
        assert response.data["is_admin"] == False
        assert response.data["is_premium"] == False
        assert len(mail.outbox) == 1

    def test_sign_up_is_successfully_but_do_not_create_an_user_with_special_fields_modified(
        self, client: APIClient
    ) -> None:
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "unusedemail2@appname.me",
            "password": "strongpassword",
            "password_confirmation": "strongpassword",
            "phone_number": "+34612123123",
            "is_verified": True,
            "is_admin": True,
            "is_premium": True,
        }
        # Normal and admin user already in database
        assert User.objects.count() == 0
        response: Response = client.post(
            f"{ENDPOINT}/signup/", data, format="json"
        )
        assert User.objects.count() == 1
        assert response.status_code == 201
        assert response.data["first_name"] == data["first_name"]
        assert response.data["last_name"] == data["last_name"]
        assert response.data["email"] == data["email"]
        assert response.data["phone_number"] == None
        assert response.data["is_verified"] == False
        assert response.data["is_admin"] == False
        assert response.data["is_premium"] == False
        assert len(mail.outbox) == 1


@pytest.mark.django_db
class TestUserLogInEndpoint:
    def test_login_fails_with_wrong_email(self, client: APIClient) -> None:
        data: dict = {
            "email": "wroongemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        message: str = "Invalid credentials"
        assert response.status_code == 400
        assert message in response.data["non_field_errors"][0]

    def test_login_fails_with_wrong_password(self, client: APIClient) -> None:
        UserFactory(email="rightemail@appname.me", password="RightPassword")
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "WrongPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        message: str = "Invalid credentials"
        assert response.status_code == 400
        assert message in response.data["non_field_errors"][0]

    def test_login_fails_with_user_not_verified(
        self, client: APIClient
    ) -> None:
        UserFactory(email="rightemail@appname.me", password="RightPassword")
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        message: str = "User is not verified"
        assert response.status_code == 400
        assert message in response.data["non_field_errors"][0]

    def test_log_in_is_successful_with_a_verified_user(
        self, client: APIClient
    ) -> None:
        testing_user: User = VerifiedUserFaker(
            email="rightemail@appname.me", password="RightPassword"
        )
        data: dict = {
            "email": "rightemail@appname.me",
            "password": "RightPassword",
        }
        response: Response = client.post(
            f"{ENDPOINT}/login/", data, format="json"
        )
        assert response.status_code == 200
        data: dict = json.loads(response.content)
        assert "token" in data
        assert "user" in data
        assert data["user"]["first_name"] == testing_user.first_name
        assert data["user"]["last_name"] == testing_user.last_name
        assert data["user"]["email"] == testing_user.email


@pytest.mark.django_db
class TestUserListEndpoint:
    def test_list_users_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 401

    def test_list_users_fails_as_an_authenticated_unverified_normal_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 403

    def test_list_users_fails_as_an_authenticated_verified_normal_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 403

    def test_list_users_is_successful_as_an_admin_user(
        self, client: APIClient
    ) -> None:
        admin_user: User = AdminFaker()
        client.force_authenticate(user=admin_user)
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_list_users_is_successful_as_an_admin_user_paginating(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=admin_user)
        url: str = f"{ENDPOINT}/?page=1&page_size=1"
        response: Response = client.get(url, format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        admin_name = admin_user.first_name
        assert response.data["results"][0]["first_name"] == admin_name
        url: str = f"{ENDPOINT}/?page=2&page_size=1"
        response: Response = client.get(url, format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        admin_name = user.first_name
        assert response.data["results"][0]["first_name"] == admin_name


@pytest.mark.django_db
class TestUserGetEndpoint:
    def test_get_user_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        response: Response = client.get(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 401

    def test_get_user_fails_as_an_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 403

    def test_get_user_fails_as_an_authenticated_verified_user_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(
            f"{ENDPOINT}/{admin_user.id}/", format="json"
        )
        assert response.status_code == 403

    def test_get_user_is_successful_as_an_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.get(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 200
        assert response.data["id"] == normal_user.id
        assert response.data["email"] == normal_user.email

    def test_get_user_is_successful_to_other_users_data_as_admin(
        self, client: APIClient
    ) -> None:
        admin_user: User = AdminFaker()
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=admin_user)
        response: Response = client.get(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserUpdateEndpoint:
    def test_update_user_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 401

    def test_update_user_fails_as_an_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 403

    def test_update_user_fails_as_an_authenticated_verified_user_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{admin_user.id}/", data, format="json"
        )
        assert response.status_code == 403
        assert normal_user.email != data["email"]

    def test_update_user_is_successful_as_an_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test edited",
            "last_name": "Tested Edit",
            "email": "edituser2@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "NewPassword95",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.email == data["email"]
        assert normal_user.phone_number == data["phone_number"]
        assert normal_user.first_name == data["first_name"]
        assert normal_user.last_name == data["last_name"]
        assert normal_user.check_password(data["password"]) is True

    def test_update_user_fails_as_an_authenticated_verified_user_with_an_used_email(
        self, client: APIClient
    ) -> None:
        UserFaker(email="emailused@appname.me")
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailused@appname.me",
            "password": "password",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 400
        assert "Email is taken" in response.data

    def test_update_user_fails_as_an_authenticated_verified_user_with_an_used_phone_number(
        self, client: APIClient
    ) -> None:
        UserFactory(phone_number="+13999999999")
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "edituser3@appname.me",
            "password": "password",
            "phone_number": "+13999999999",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 400
        assert "Phone number is taken" in response.data

    def test_update_user_fails_as_an_authenticated_verified_user_with_a_wrong_old_password(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "finalemail@appname.me",
            "phone_number": "+32987654321",
            "old_password": "NewPassword95 wrong",
            "password": "This is a password",
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        message: str = "Wrong password"
        assert response.status_code == 400
        assert message in response.data

    def test_update_user_fails_as_an_authenticated_verified_user_without_old_password(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "finalemail@appname.me",
            "phone_number": "+32987654321",
            "password": "This is a password",
        }
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        message: str = "Old password is required to set a new one"
        assert response.status_code == 400
        assert message in response.data

    def test_update_user_is_successful_as_an_authenticated_verified_user_with_just_a_new_password(
        self, client: APIClient
    ) -> None:
        data: dict = {"old_password": "password", "password": "New Password"}
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.check_password(data["password"]) is True

    def test_update_user_is_successful_as_an_authenticated_verified_user_but_do_not_change_special_fields(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailemail@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "New password",
            "is_verified": False,
            "is_admin": True,
            "is_premium": True,
        }
        client.force_authenticate(user=normal_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.email == data["email"]
        assert normal_user.phone_number == data["phone_number"]
        assert normal_user.first_name == data["first_name"]
        assert normal_user.last_name == data["last_name"]
        assert normal_user.check_password(data["password"]) is True
        assert normal_user.is_verified is True
        assert normal_user.is_admin is False
        assert normal_user.is_premium is False

    def test_update_user_is_successful_as_admin_to_other_user_data_but_do_not_change_special_fields(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailemail@appname.me",
            "phone_number": "+32987654321",
            "old_password": "password",
            "password": "New password",
            "is_verified": False,
            "is_admin": True,
            "is_premium": True,
        }
        client.force_authenticate(user=admin_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.email == data["email"]
        assert normal_user.phone_number == data["phone_number"]
        assert normal_user.first_name == data["first_name"]
        assert normal_user.last_name == data["last_name"]
        assert normal_user.check_password(data["password"]) is True
        assert normal_user.is_verified is True
        assert normal_user.is_admin is False
        assert normal_user.is_premium is False

    def test_update_user_fails_with_wrong_phone_format(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        data: dict = {
            "first_name": "Test",
            "last_name": "Tested",
            "email": "emailemail@appname.me",
            "phone_number": "32987654321",
            "old_password": "password",
            "password": "New password",
            "is_verified": False,
            "is_admin": True,
            "is_premium": True,
        }
        client.force_authenticate(user=admin_user)
        response: Response = client.put(
            f"{ENDPOINT}/{normal_user.id}/", data, format="json"
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestUserDeleteEndpoint:
    def test_delete_user_fails_as_an_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        assert User.objects.count() == 1
        response: Response = client.delete(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 401
        assert User.objects.count() == 1

    def test_delete_user_fails_as_an_authenticated_unverified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.delete(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 403
        assert User.objects.count() == 1

    def test_delete_user_fails_as_an_authenticated_verified_user_to_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = UserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.delete(
            f"{ENDPOINT}/{admin_user.id}/", format="json"
        )
        assert response.status_code == 403
        assert User.objects.count() == 2

    def test_delete_user_is_successful_as_an_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        client.force_authenticate(user=normal_user)
        response: Response = client.delete(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 204
        assert User.objects.count() == 0

    def test_delete_user_is_successful_as_admin_to_other_users_data(
        self, client: APIClient
    ) -> None:
        normal_user: User = VerifiedUserFaker()
        admin_user: User = AdminFaker()
        client.force_authenticate(user=admin_user)
        response: Response = client.delete(
            f"{ENDPOINT}/{normal_user.id}/", format="json"
        )
        assert response.status_code == 204
        assert User.objects.count() == 1


@pytest.mark.django_db
class TestUserVerifyEndpoint:
    def test_verify_user(self, client: APIClient) -> None:
        # Test that any user can verify its user with a get
        # request with it id and token
        assert Profile.objects.count() == 0
        normal_user: User = UserFaker()
        token = generate_user_verification_token(normal_user)
        assert normal_user.is_verified is False
        response: Response = client.get(
            f"{ENDPOINT}/{normal_user.id}/verify/?token={token}"
        )
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.is_verified is True
        assert Profile.objects.count() == 1
        assert normal_user.profile is not None


@pytest.mark.django_db
class TestUserPasswordResetTests:
    def test_reset_password(self, client: APIClient) -> None:
        # Test that any user can reset its password via API
        normal_user: User = UserFaker()
        assert normal_user.check_password("password") is True
        response: Response = client.post(
            f"/api/password_reset/", {"email": normal_user.email}
        )
        assert response.status_code == 200
        tokens: ResetPasswordToken = ResetPasswordToken.objects.all()
        assert len(tokens) == 1
        token: int = tokens[0].key
        data: dict = {"token": token, "password": "NewPassword95"}
        client.post(f"/api/password_reset/confirm/", data, format="json")
        assert response.status_code == 200
        normal_user.refresh_from_db()
        assert normal_user.check_password("NewPassword95") is True
        assert len(mail.outbox) == 1
