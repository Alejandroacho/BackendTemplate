from django_rest_passwordreset.models import ResetPasswordToken

from App.utils import log_email_action
from Emails.factories.email import ResetEmailFactory
from Emails.factories.email import VerifyEmailFactory
from Emails.models.models import Email
from Users.models import User


def send_email(email_type: str, instance: User or ResetPasswordToken) -> None:
    if email_type == "verify_email":
        email: Email = VerifyEmailFactory(instance=instance)
    elif email_type == "reset_password":
        email: Email = ResetEmailFactory(instance=instance)
    email.send()
    log_email_action(email_type, instance)
