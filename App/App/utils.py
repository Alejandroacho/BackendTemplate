import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def log_information(event, instance):
    """
    Log information about an action over an instance
    """
    now = datetime.now()
    class_name = instance.__class__.__name__
    introduction = f'{class_name}s App | {class_name}'
    message = f'{introduction} "{instance.id}" {event} at {now}'
    logger.info(message)


def log_email_action(email_type, instance):
    if email_type == 'verify_email':
        logger.info(
            'Users App | New user, verification email sent to '
            f'{instance.email} at {datetime.now()}'
        )
    else:
        logger.info(
            'Users App | Password restore, email sent to '
            f'{instance.user.email} at {datetime.now()}'
        )
