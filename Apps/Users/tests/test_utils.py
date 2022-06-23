import pytest
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError
from Users.factories.user import UserFactory
from Users.models import User
from Users.utils import check_e164_format
from Users.utils import generate_user_verification_token
from Users.utils import verify_user_query_token


@pytest.mark.django_db
class TestUserUtils:
    def test_verify_user_query_token_raises_PermissionDenied(self) -> None:
        user: User = UserFactory()
        token: str = "Wrong token"
        with pytest.raises(PermissionDenied):
            verify_user_query_token(user, token)

    def test_generate_user_verification_token_function(self) -> None:
        user: User = UserFactory()
        token: str = generate_user_verification_token(user)
        assert type(token) == str
        assert len(token) > 10

    def test_verify_user_query_token_do_not_raise_anything(self) -> None:
        user: User = UserFactory()
        token: str = generate_user_verification_token(user)
        verify_user_query_token(user, token)

    def test_check_e164_format_raises_PermissionDenied(self) -> None:
        phone_number: str = "000000000"
        with pytest.raises(ValidationError):
            check_e164_format(phone_number)

    def test_check_e164_format_do_not_raises_PermissionDenied(self) -> None:
        phone_number: str = "+00000000000"
        check_e164_format(phone_number)
