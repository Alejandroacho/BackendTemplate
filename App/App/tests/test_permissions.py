import pytest
from mock import MagicMock
from mock import PropertyMock

from App.permissions import IsActionAllowed
from App.permissions import IsAdmin
from App.permissions import IsProfileOwner
from App.permissions import IsSameUserId
from App.permissions import IsUserOwner
from App.permissions import IsVerified
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.models import Profile


@pytest.mark.django_db
class TestIsAdminPermission:
    def test_returns_false_if_user_is_not_admin(self):
        requester = UserFaker()
        assert requester.is_admin is False
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsAdmin().has_permission(request, None) is False

    def test_returns_true_if_user_is_admin(self):
        requester = AdminFaker()
        assert requester.is_admin is True
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsAdmin().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsVerifiedPermission:
    def test_returns_false_if_user_is_not_verified(self):
        requester = UserFaker()
        assert requester.is_verified is False
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsVerified().has_permission(request, None) is False

    def test_returns_true_if_user_is_verified(self):
        requester = VerifiedUserFaker()
        assert requester.is_verified is True
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsVerified().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsUserOwnerPermission:
    def test_returns_false_if_user_is_not_owner(self):
        user = UserFaker()
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'kwargs': {'pk': user.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        type(request).parser_context = mocked_kwargs
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsUserOwner().has_permission(request, None) is False

    def test_returns_true_if_user_is_owner(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'kwargs': {'pk': requester.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsUserOwner().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsSameUserId:
    def test_returns_false_if_user_id_in_url_is_not_the_requester_id(self):
        user = VerifiedUserFaker()
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'user_id': f'{user.id}'}
        mocked_url_kwargs = PropertyMock(return_value=kwargs)
        type(request).GET = mocked_url_kwargs
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsSameUserId().has_permission(request, None) is False

    def test_returns_true_if_user_id_in_url_is_the_requester_id(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'user_id': requester.id}
        mocked_url_kwargs = PropertyMock(return_value=kwargs)
        type(request).GET = mocked_url_kwargs
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        assert IsSameUserId().has_permission(request, None) is True

    def test_returns_true_without_user_id_in_url(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        mocked_url_kwargs = PropertyMock(return_value={})
        type(request).GET = mocked_url_kwargs
        assert IsSameUserId().has_permission(request, None) is True


@pytest.mark.django_db
class TestIsProfileOwnerPermission:
    def test_returns_true_if_profile_is_from_user(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        kwargs = {'kwargs': {'pk': requester.profile.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is True

    def test_returns_false_if_profile_is_not_from_user(self):
        requester = VerifiedUserFaker()
        other_user = VerifiedUserFaker(email='other@user.com')
        request = MagicMock()
        kwargs = {'kwargs': {'pk': other_user.profile.id}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is False

    def test_returns_false_if_profile_do_not_exists(self):
        requester = VerifiedUserFaker()
        request = MagicMock()
        last_profile = Profile.objects.all().last()
        kwargs = {'kwargs': {'pk': last_profile.id + 1}}
        mocked_kwargs = PropertyMock(return_value=kwargs)
        mocked_requester = PropertyMock(return_value=requester)
        type(request).user = mocked_requester
        type(request).parser_context = mocked_kwargs
        assert IsProfileOwner().has_permission(request, None) is False


@pytest.mark.django_db
class TestIsActionAllowedPermission:
    def test_returns_true_for_retrieve_action_allowed(self):
        view = MagicMock()
        action = 'retrieve'
        mocked_action = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is True

    def test_returns_true_for_update_action_allowed(self):
        view = MagicMock()
        action = 'update'
        mocked_action = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is True

    def test_returns_false_for_list_action_not_allowed(self):
        view = MagicMock()
        action = 'list'
        mocked_action = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is False

    def test_returns_false_for_create_action_not_allowed(self):
        view = MagicMock()
        action = 'create'
        mocked_action = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is False

    def test_returns_false_for_delete_action_not_allowed(self):
        view = MagicMock()
        action = 'delete'
        mocked_action = PropertyMock(return_value=action)
        type(view).action = mocked_action
        assert IsActionAllowed().has_permission(None, view) is False
