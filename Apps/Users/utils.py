import base64
import hashlib
import re as regex

from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from Users.models import User


def generate_user_verification_token(user: User) -> str:
    """
    Creates an user token to verify its account
    """
    string_user: str = user.email + settings.EMAIL_VERIFICATION_TOKEN_SECRET
    hashed: str = hashlib.sha256(string_user.encode())
    decoded: str = base64.b64encode(hashed.digest()).decode("utf-8")
    token: str = (
        decoded.replace("\\", "-")
        .replace("/", "_")
        .replace("=", "")
        .replace("+", "")
    )
    return token


def verify_user_query_token(user: User, query_token: str) -> None:
    """
    Verify user token to verification account
    """
    token: str = generate_user_verification_token(user)
    if token != query_token:
        raise PermissionDenied("You don't have permission")


def check_e164_format(phone_number: str) -> None:
    """
    Checks if a phone number is in E.164 format
    example: +11234567890
    """
    regex_format: str = r"^\+[0-9]\d{1,20}$"
    if phone_number and not regex.match(regex_format, phone_number):
        raise ValidationError("Phone number is not valid")
