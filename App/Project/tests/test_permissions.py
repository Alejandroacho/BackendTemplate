import pytest
from mock import MagicMock
from mock import PropertyMock

from Project.permissions import IsActionAllowed
from Project.permissions import IsAdmin
from Project.permissions import IsProfileOwner
from Project.permissions import IsSameUserId
from Project.permissions import IsUserOwner
from Project.permissions import IsVerified
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile
from Users.models import User


@pytest.mark.django_db
class TestIsAdminPermission:
    def test_returns_false_if_user_is_not_admin(self) -> None:
        requester: User = UserFaker()
        assert requester.is_admin is False
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsAdmin().has_permission(request, None) is False

    def test_returns_true_if_user_is_admin(self) -> None:
        requester: User = AdminFaker()
        assert requester.is_admin is True
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsAdmin().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsVerifiedPermission:
    def test_returns_false_if_user_is_not_verified(self) -> None:
        requester: User = UserFaker()
        assert requester.is_verified is False
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsVerified().has_permission(request, None) is False

    def test_returns_true_if_user_is_verified(self) -> None:
        requester: User = VerifiedUserFaker()
        assert requester.is_verified is True
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsVerified().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsUserOwnerPermission:
    def test_returns_false_if_user_is_not_owner(self) -> None:
        user: User = UserFaker()
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        kwargs: dict = {"kwargs": {"pk": user.id}}
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        type(request).parser_context = mocked_kwargs
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsUserOwner().has_permission(request, None) is False

    def test_returns_true_if_user_is_owner(self) -> None:
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        kwargs: dict = {"kwargs": {"pk": requester.id}}
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsUserOwner().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsSameUserId:
    def test_returns_false_if_user_id_in_url_is_not_the_requester_id(
        self,
    ) -> None:
        user: User = VerifiedUserFaker()
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        kwargs: dict = {"user_id": f"{user.id}"}
        mocked_url_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        type(request).GET = mocked_url_kwargs
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsSameUserId().has_permission(request, None) is False

    def test_returns_true_if_user_id_in_url_is_the_requester_id(self) -> None:
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        kwargs: dict = {"user_id": requester.id}
        mocked_url_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        type(request).GET = mocked_url_kwargs
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsSameUserId().has_permission(request, None) is True

    def test_returns_true_without_user_id_in_url(self) -> None:
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        mocked_url_kwargs: PropertyMock = PropertyMock(return_value={})
        type(request).GET = mocked_url_kwargs
        assert IsSameUserId().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsProfileOwnerPermission:
    def test_returns_true_if_profile_is_from_user(self) -> None:
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        kwargs: dict = {"kwargs": {"pk": requester.profile.id}}
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is True

    def test_returns_false_if_profile_is_not_from_user(self) -> None:
        requester: User = VerifiedUserFaker()
        other_user: User = VerifiedUserFaker(email="other@user.com")
        request: MagicMock = MagicMock()
        kwargs: dict = {"kwargs": {"pk": other_user.profile.id}}
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is False

    def test_returns_false_if_profile_do_not_exists(self) -> None:
        requester: User = VerifiedUserFaker()
        request: MagicMock = MagicMock()
        last_profile: Profile = Profile.objects.all().last()
        kwargs: dict = {"kwargs": {"pk": last_profile.id + 1}}
        mocked_kwargs: PropertyMock = PropertyMock(return_value=kwargs)
        mocked_requester: PropertyMock = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is False


@pytest.mark.django_db
class TestIsActionAllowedPermission:
    def test_returns_true_for_retrieve_action_allowed(self) -> None:
        view: MagicMock = MagicMock()
        action: str = "retrieve"
        mocked_action: PropertyMock = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is True

    def test_returns_true_for_update_action_allowed(self) -> None:
        view: MagicMock = MagicMock()
        action: str = "update"
        mocked_action: PropertyMock = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is True

    def test_returns_false_for_list_action_not_allowed(self) -> None:
        view: MagicMock = MagicMock()
        action: str = "list"
        mocked_action: PropertyMock = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is False

    def test_returns_false_for_create_action_not_allowed(self) -> None:
        view: MagicMock = MagicMock()
        action: str = "create"
        mocked_action: PropertyMock = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is False

    def test_returns_false_for_delete_action_not_allowed(self) -> None:
        view: MagicMock = MagicMock()
        action: str = "delete"
        mocked_action: PropertyMock = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is False
