import logging
from datetime import datetime
from logging import Logger

import pytest
from freezegun import freeze_time
from mock import MagicMock
from mock import PropertyMock

from Project.utils import log_email_action
from Project.utils import log_information


@pytest.mark.django_db
class TestAppUtils:
    @freeze_time("2012-01-14")
    def test_log_information(self, caplog: Logger) -> None:
        caplog.clear()
        caplog.set_level(logging.INFO)
        instance: MagicMock = MagicMock()
        id: PropertyMock = PropertyMock(return_value=1)
        type(instance).id = id
        log_information("test", instance)
        now: datetime = datetime.now()
        introduction: str = f"MagicMocks App | MagicMock"
        test_instance: int = 1
        expected_message: str = (
            f'{introduction} "{test_instance}" test at {now}'
        )
        assert expected_message in caplog.text

    @freeze_time("2012-01-14")
    def test_log_email_verification_action_on_verify(
        self, caplog: Logger
    ) -> None:
        caplog.clear()
        caplog.set_level(logging.INFO)
        instance: MagicMock = MagicMock()
        email: PropertyMock = PropertyMock(return_value="test@test.com")
        type(instance).email = email
        log_email_action("verify_email", instance)
        now: datetime = datetime.now()
        expected_message: str = (
            f"Users App | New user, verification "
            + f"email sent to test@test.com at {now}"
        )
        assert expected_message in caplog.text

    @freeze_time("2012-01-14")
    def test_log_email_verification_action_on_restore(
        self, caplog: Logger
    ) -> None:
        caplog.clear()
        caplog.set_level(logging.INFO)
        instance: MagicMock = MagicMock()
        user: MagicMock = MagicMock()
        email: PropertyMock = PropertyMock(return_value="test@test.com")
        type(instance).user = user
        type(user).email = email
        log_email_action("restore", instance)
        now: datetime = datetime.now()
        expected_message: str = (
            f"Users App | Password restore, email "
            + f"sent to test@test.com at {now}"
        )
        assert expected_message in caplog.text
