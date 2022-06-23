import base64
from io import BufferedReader

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from Users.factories.user import UserFactory
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User


ENDPOINT: str = "/api/profiles"


@pytest.fixture(scope="function")
def client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="class")
def base64_image() -> bytes:
    image_file: BufferedReader = open("Project/static/logo.png", "rb")
    image_base64: bytes = base64.b64encode(image_file.read())
    image_file.close()
    return image_base64


@pytest.mark.django_db
class TestProfileListEndpoint:
    def test_list_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 401

    def test_list_fails_as_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        client.force_authenticate(user=user)
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 403

    def test_list_fails_as_authenticated_verified_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        client.force_authenticate(user=user)
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 403

    def test_list_success_as_admin_user(self, client: APIClient) -> None:
        user: User = AdminFaker()
        client.force_authenticate(user=user)
        response: Response = client.get(f"{ENDPOINT}/", format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == Profile.objects.count()
        assert response.data["count"] == Profile.objects.count()


@pytest.mark.django_db
class TestProfileRetrieveEndpoint:
    def test_retrieve_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        user.create_profile()
        profile_id: int = user.profile.id
        response: Response = client.get(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 401

    def test_retrieve_fails_as_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        user: User = UserFaker()
        user.create_profile()
        client.force_authenticate(user=user)
        profile_id: int = user.profile.id
        response: Response = client.get(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 403

    def test_retrieve_fails_as_authenticated_verified_user_to_other_user_data(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        other_user: User = UserFactory(
            email="other@user.com", is_verified=True
        )
        client.force_authenticate(user=user)
        profile_id: int = other_user.profile.id
        response: Response = client.get(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 403

    def test_retrieve_success_as_authenticated_verified_user_to_its_data(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        client.force_authenticate(user=user)
        profile_id: int = user.profile.id
        response: Response = client.get(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        profile: Profile = user.profile
        assert response.status_code == 200
        assert response.data["id"] == profile_id
        assert response.data["user_id"] == user.id
        assert response.data["nickname"] == profile.nickname
        assert response.data["bio"] == profile.bio
        assert response.data["gender"] == profile.gender
        assert (
            response.data["preferred_language"] == profile.preferred_language
        )
        assert response.data["image"] == profile.image
        assert response.data["birth_date"] == profile.birth_date
        assert response.data["is_adult"] == profile.is_adult()

    def test_retrieve_success_as_admin_to_other_user_data(
        self, client: APIClient
    ) -> None:
        assert 0 == Profile.objects.count()
        user: User = VerifiedUserFaker()
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        profile_id: int = user.profile.id
        response: Response = client.get(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        profile: Profile = user.profile
        assert response.status_code == 200
        assert response.data["id"] == profile_id
        assert response.data["user_id"] == user.id
        assert response.data["nickname"] == profile.nickname
        assert response.data["bio"] == profile.bio
        assert response.data["gender"] == profile.gender
        assert (
            response.data["preferred_language"] == profile.preferred_language
        )
        assert response.data["image"] == profile.image
        assert response.data["birth_date"] == profile.birth_date
        assert response.data["is_adult"] == profile.is_adult()


@pytest.mark.django_db
class TestProfileCreateEndpoint:
    def test_create_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        data: dict = {}
        response: Response = client.post(
            f"{ENDPOINT}/", data=data, format="json"
        )
        assert response.status_code == 401

    def test_create_fails_as_authenticated_unverified_user(
        self, client
    ) -> None:
        data: dict = {}
        user: User = UserFaker()
        client.force_authenticate(user=user)
        response: Response = client.post(
            f"{ENDPOINT}/", data=data, format="json"
        )
        assert response.status_code == 403

    def test_create_fails_as_authenticated_verified_user(
        self, client: APIClient
    ) -> None:
        # create will be triggered when verifying the user instance
        # so the create method will be available only for admin users
        user: User = UserFaker()
        data: dict = {"user_id": user.pk, "nickname": "test", "bio": "test"}
        user: User = VerifiedUserFaker()
        client.force_authenticate(user=user)
        response: Response = client.post(
            f"{ENDPOINT}/", data=data, format="json"
        )
        assert response.status_code == 403

    def test_create_fails_with_used_user_id_as_admin(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {"user_id": user.pk, "nickname": "test", "bio": "test"}
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.post(
            f"{ENDPOINT}/", data=data, format="json"
        )
        error_message: str = "User profile already exists"
        assert response.status_code == 400
        assert response.data == [error_message]

    def test_create_fails_with_used_nickname_as_admin(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        profile: Profile = user.profile
        profile.nickname = "test"
        profile.save()
        other_user: User = UserFaker()
        data: dict = {
            "user_id": other_user.pk,
            "nickname": user.profile.nickname,
        }
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.post(
            f"{ENDPOINT}/", data=data, format="json"
        )
        error_message: str = "This nickname already exists."
        assert response.status_code == 400
        assert response.data["nickname"] == [error_message]

    def test_create_success_as_admin(self, client: APIClient) -> None:
        user: User = UserFaker()
        data: str = {"user_id": user.pk, "nickname": "test", "bio": "test"}
        admin: User = AdminFaker()
        client.force_authenticate(user=admin)
        response: Response = client.post(
            f"{ENDPOINT}/", data=data, format="json"
        )
        assert response.status_code == 201
        user.refresh_from_db()
        assert response.data["id"] == user.profile.id
        assert response.data["user_id"] == data["user_id"]
        assert response.data["nickname"] == data["nickname"]
        assert response.data["bio"] == data["bio"]


@pytest.mark.django_db
class TestProfileUpdateEndpoint:
    def test_update_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {}
        profile_id: int = user.profile.id
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 401

    def test_update_fails_as_authenticated_unverified_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {}
        profile_id: int = user.profile.id
        user.is_verified = False
        user.save()
        client.force_authenticate(user=user)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 403

    def test_update_fails_as_authenticated_verified_user_to_other_user_profile(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        other_user: User = VerifiedUserFaker(email="other@email.com")
        data: dict = {}
        profile_id: int = other_user.profile.id
        client.force_authenticate(user=user)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 403

    def test_update_success_as_authenticated_verified_user_to_its_profile(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        data: dict = {
            "nickname": "testing nickname",
            "bio": "testing bio",
        }
        profile_id: int = user.profile.id
        client.force_authenticate(user=user)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 200
        assert response.data["id"] == profile_id
        assert response.data["user_id"] == user.id
        assert response.data["nickname"] == data["nickname"]
        assert response.data["bio"] == data["bio"]

    def test_update_success_as_authenticate_verified_user_to_its_profile_do_not_change_the_user_id(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker(email="other@usertesting.com")
        other_user.profile.delete()
        user: User = VerifiedUserFaker()
        data: dict = {
            "user_id": other_user.pk,
            "nickname": "testing nickname",
            "bio": "testing bio",
        }
        profile_id: int = user.profile.id
        client.force_authenticate(user=user)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 200
        assert response.data["id"] == profile_id
        assert response.data["user_id"] == user.id
        assert response.data["nickname"] == data["nickname"]
        assert response.data["bio"] == data["bio"]

    def test_update_success_as_authenticate_verified_user_to_its_profile_changes_image(
        self, client: APIClient, base64_image: bytes
    ) -> None:
        user: User = VerifiedUserFaker()
        assert user.profile.image.name is None
        data: dict = {
            "image": base64_image,
            "nickname": "testing nickname",
            "bio": "testing bio",
        }
        profile_id: int = user.profile.id
        client.force_authenticate(user=user)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 200
        assert response.data["id"] == profile_id
        assert response.data["image"] is not None
        assert response.data["user_id"] == user.id
        assert response.data["nickname"] == data["nickname"]
        assert response.data["bio"] == data["bio"]
        user.refresh_from_db()
        assert user.profile.image.name is not None

    def test_update_success_as_admin_can_change_user_id(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker(email="other@usertesting.com")
        other_user.profile.delete()
        user: User = VerifiedUserFaker()
        admin: User = AdminFaker()
        data: dict = {
            "user_id": other_user.pk,
            "nickname": "testing nickname",
            "bio": "testing bio",
        }
        assert user.profile is not None
        profile_id: int = user.profile.id
        client.force_authenticate(user=admin)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 200
        assert response.data["id"] == profile_id
        assert response.data["user_id"] == other_user.id
        assert response.data["nickname"] == data["nickname"]
        assert response.data["bio"] == data["bio"]
        user.refresh_from_db()
        assert getattr(user, "profile", None) is None

    def test_update_fails_as_admin_changing_to_used_user_id(
        self, client: APIClient
    ) -> None:
        other_user: User = VerifiedUserFaker(email="other@usertesting.com")
        user: User = VerifiedUserFaker()
        admin: User = AdminFaker()
        data: dict = {
            "user_id": other_user.pk,
            "nickname": "testing nickname",
            "bio": "testing bio",
        }
        profile_id: int = user.profile.id
        client.force_authenticate(user=admin)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 400
        error_message = "User profile already exists"
        assert response.data == [error_message]

    def test_update_success_as_admin_not_changing_user_id(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        admin: User = AdminFaker()
        data: dict = {
            "user_id": user.pk,
            "nickname": "testing nickname",
            "bio": "testing bio",
        }
        profile_id: int = user.profile.id
        client.force_authenticate(user=admin)
        response: Response = client.put(
            f"{ENDPOINT}/{profile_id}/", data=data, format="json"
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestProfileDeleteEndpoint:
    def test_delete_fails_as_unauthenticated_user(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        profile_id: int = user.profile.id
        response: Response = client.delete(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 401

    def test_delete_fails_as_authenticated_unverified_user(self, client):
        user: User = VerifiedUserFaker()
        profile_id: int = user.profile.id
        user.is_verified = False
        user.save()
        client.force_authenticate(user=user)
        response: Response = client.delete(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 403

    def test_delete_fails_as_authenticated_verified_user_to_other_user_profile(
        self, client: APIClient
    ) -> None:
        user: User = VerifiedUserFaker()
        other_user: User = VerifiedUserFaker(email="other@email.com")
        profile_id: int = other_user.profile.id
        client.force_authenticate(user=user)
        response: Response = client.delete(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 403

    def test_delete_fails_as_authenticate_verified_user_to_its_profile(
        self, client: APIClient
    ) -> None:
        # destroy will be triggered when deleted the user instance
        # so the destroy method will be available only for admin users
        user: User = VerifiedUserFaker()
        profile_id: int = user.profile.id
        client.force_authenticate(user=user)
        response: Response = client.delete(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 403

    def test_delete_success_as_admin(self, client: APIClient) -> None:
        admin: User = AdminFaker(is_verified=False)
        # not verified to avoid profile creation
        user: User = VerifiedUserFaker()
        profile_id: int = user.profile.id
        client.force_authenticate(user=admin)
        assert Profile.objects.count() == 1
        response: Response = client.delete(
            f"{ENDPOINT}/{profile_id}/", format="json"
        )
        assert response.status_code == 204
        assert Profile.objects.count() == 0
