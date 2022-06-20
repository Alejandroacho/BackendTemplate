from App.utils import log_email_action
from Emails.factories.email import ResetEmailFactory
from Emails.factories.email import VerifyEmailFactory


def send_email(email_type, instance):
    if email_type == 'verify_email':
        email = VerifyEmailFactory(instance=instance)
    elif email_type == 'reset_password':
        email = ResetEmailFactory(instance=instance)
    email.send()
    log_email_action(email_type, instance)
