import logging
from datetime import datetime
from logging import Logger

from django.db.models import Model


logger: Logger = logging.getLogger(__name__)


def log_information(event: str, instance: Model) -> None:
    """
    Log information about an action over an instance
    """
    now: datetime = datetime.now()
    class_name: str = instance.__class__.__name__
    introduction: str = f"{class_name}s App | {class_name}"
    message: str = f'{introduction} "{instance.id}" {event} at {now}'
    logger.info(message)


def log_email_action(email_type: str, instance: Model) -> None:
    if email_type == "verify_email":
        logger.info(
            "Users App | New user, verification email sent to "
            f"{instance.email} at {datetime.now()}"
        )
    else:
        logger.info(
            "Users App | Password restore, email sent to "
            f"{instance.user.email} at {datetime.now()}"
        )
