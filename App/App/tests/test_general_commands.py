import pytest
from django.core.management import call_command
from django.test import override_settings

from App.management.commands.populate_db import Command as PopulateCommand
from Emails.models.models import Email
from Emails.models.models import Suggestion
from Users.factories.user import UserFactory
from Users.models import Profile
from Users.models import User


COMMAND = 'populate_db'


@pytest.mark.django_db
class TestPopulateCommand:
    @override_settings(ENVIRONMENT_NAME='production')
    def test_populate_db_command_fails_on_non_dev_mode(self, caplog):
        caplog.clear()
        call_command(COMMAND, '-i', '5')
        message = (
            'This command creates fake data do NOT run '
            + 'this in production environments'
        )
        assert [message] == [record.message for record in caplog.records]

    def test_create_fake_users(self):
        command = PopulateCommand()
        assert User.objects.all().count() == 0
        command.create_fake_users(3)
        assert User.objects.all().count() == 3

    def test_create_fake_verify_emails(self):
        command = PopulateCommand()
        users = [UserFactory(), UserFactory()]
        assert User.objects.all().count() == 2
        assert Email.objects.all().count() == 0
        command.create_fake_verify_emails(users)
        assert User.objects.all().count() == 2
        assert Email.objects.all().count() == 2

    def test_create_fake_profiles(self):
        command = PopulateCommand()
        users = [UserFactory(), UserFactory()]
        assert User.objects.all().count() == 2
        assert Profile.objects.all().count() == 0
        command.create_fake_profiles(users)
        assert User.objects.all().count() == 2
        assert Profile.objects.all().count() == 2

    def test_create_fake_suggestions(self):
        command = PopulateCommand()
        users = [UserFactory(), UserFactory()]
        assert User.objects.all().count() == 2
        assert Suggestion.objects.all().count() == 0
        command.create_fake_suggestions(users)
        assert User.objects.all().count() == 2
        assert Suggestion.objects.all().count() == 2

    def test_create_admin_user(self):
        command = PopulateCommand()
        assert User.objects.filter(is_admin=True).count() == 0
        command.create_admin_user()
        assert User.objects.filter(is_admin=True).count() == 1

    def test_command_without_admin_flag(self):
        assert User.objects.all().count() == 0
        assert Email.objects.all().count() == 0
        assert Profile.objects.all().count() == 0
        assert Suggestion.objects.all().count() == 0
        call_command(COMMAND, '-i', '5')
        assert User.objects.all().count() == 6
        assert Email.objects.all().count() == 5
        assert Profile.objects.all().count() == 6
        assert Suggestion.objects.all().count() == 5

    def test_command_with_admin_flag_in_false(self):
        assert User.objects.all().count() == 0
        assert Email.objects.all().count() == 0
        assert Profile.objects.all().count() == 0
        assert Suggestion.objects.all().count() == 0
        call_command(COMMAND, '-i', '5', '-n')
        assert User.objects.all().count() == 5
        assert Email.objects.all().count() == 5
        assert Profile.objects.all().count() == 5
        assert Suggestion.objects.all().count() == 5
