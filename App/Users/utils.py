import base64
import hashlib
import re as regex

from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError


def generate_user_verification_token(user):
    """
    Creates an user token to verify its account
    """
    string_user = user.email + settings.EMAIL_VERIFICATION_TOKEN_SECRET
    hashed = hashlib.md5(string_user.encode())
    decoded = base64.b64encode(hashed.digest()).decode('utf-8')
    token = (
        decoded.replace('\\', '-')
        .replace('/', '_')
        .replace('=', '')
        .replace('+', '')
    )
    return token


def verify_user_query_token(user, query_token):
    """
    Verify user token to verification account
    """
    token = generate_user_verification_token(user)
    if token != query_token:
        raise PermissionDenied("You don't have permission")


def check_e164_format(phone_number):
    """
    Checks if a phone number is in E.164 format
    example: +11234567890
    """
    regex_format = r'^\+[0-9]\d{1,20}$'
    if phone_number and not regex.match(regex_format, phone_number):
        raise ValidationError('Phone number is not valid')
