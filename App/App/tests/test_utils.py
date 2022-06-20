from datetime import datetime

from django.test import TestCase
from freezegun import freeze_time
from mock import MagicMock
from mock import PropertyMock

from App.utils import log_email_action
from App.utils import log_information


class AppUtilsTest(TestCase):
    @freeze_time('2012-01-14')
    def test_log_information(self):
        with self.assertLogs('App', level='INFO') as message:
            log_information('test', self)

        now = datetime.now()
        class_name = 'AppUtilsTest'
        introduction = f'{class_name}s App | {class_name}'
        test_instance = self.id
        expected_message = (
            f'INFO:App.utils:{introduction} "{test_instance}" test at {now}'
        )
        self.assertEqual(message.output, [expected_message])

    @freeze_time('2012-01-14')
    def test_log_email_verification_action_on_verify(self):
        instance = MagicMock()
        email = PropertyMock(return_value='test@test.com')
        type(instance).email = email
        with self.assertLogs('App', level='INFO') as message:
            log_email_action('verify_email', instance)
        now = datetime.now()
        expected_message = (
            f'INFO:App.utils:Users App | New user, verification '
            + f'email sent to test@test.com at {now}'
        )
        self.assertEqual(message.output, [expected_message])

    @freeze_time('2012-01-14')
    def test_log_email_verification_action_on_restore(self):
        instance = MagicMock()
        user = MagicMock()
        email = PropertyMock(return_value='test@test.com')
        type(instance).user = user
        type(user).email = email
        with self.assertLogs('App', level='INFO') as message:
            log_email_action('restore', instance)
        now = datetime.now()
        expected_message = (
            f'INFO:App.utils:Users App | Password restore, email '
            + f'sent to test@test.com at {now}'
        )
        self.assertEqual(message.output, [expected_message])
