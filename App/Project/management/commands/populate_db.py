import logging
from logging import Logger

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser
from tqdm import tqdm
from tqdm import trange as progress

from Emails.choices import CommentType
from Emails.factories.email import VerifyEmailFactory
from Emails.factories.suggestion import SuggestionEmailFactory
from Users.factories.profile import ProfileFactory
from Users.factories.user import UserFactory
from Users.models import User


logger: Logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help: str = "Populate database with fake data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-i", "--instances", type=int, default=50)
        parser.add_argument(
            "-n", "--no-admin", dest="admin", action="store_false"
        )
        parser.set_defaults(admin=True)

    def handle(self, *args: tuple, **options: dict) -> None:
        if settings.ENVIRONMENT_NAME in ["dev", "local", "test"]:
            instances_number: int = options["instances"]
            create_admin: bool = options["admin"]
            self.populate(instances_number, create_admin)
        else:
            logger.critical(
                "This command creates fake data do NOT run this in"
                + " production environments"
            )

    def populate(self, instances_number: int, create_admin: bool) -> None:
        users: list = self.create_fake_users(instances_number)
        self.create_fake_verify_emails(users)
        self.create_fake_profiles(users)
        self.create_fake_suggestions(users)
        if create_admin:
            self.create_admin_user()

    def create_fake_users(self, instances_number: int) -> list:
        self.stdout.write("Creating fake users")
        users: list = []
        for _ in progress(instances_number):
            user: User = UserFactory()
            users.append(user)
        self.stdout.write("Fake users created")
        return users

    def create_fake_verify_emails(self, users: list) -> None:
        self.stdout.write("Creating fake verify emails")
        with tqdm(total=len(users)) as progress_bar:
            for user in users:
                VerifyEmailFactory(instance=user)
                progress_bar.update(1)
        self.stdout.write("Fake verify emails created")

    def create_fake_profiles(self, users: list) -> None:
        self.stdout.write("Creating fake profiles")
        with tqdm(total=len(users)) as progress_bar:
            for user in users:
                ProfileFactory(user=user)
                progress_bar.update(1)
        self.stdout.write("Fake profiles created")

    def create_fake_suggestions(self, users: list) -> None:
        self.stdout.write("Creating fake suggestions")
        type: str = CommentType.SUGGESTION.value
        content: str = "This is a fake suggestion"
        with tqdm(total=len(users)) as progress_bar:
            for user in users:
                SuggestionEmailFactory(type=type, content=content, user=user)
                progress_bar.update(1)
        self.stdout.write("Fake profiles created")

    def create_admin_user(self) -> None:
        self.stdout.write("Creating admin user")
        UserFactory(
            is_admin=True,
            email="admin@admin.com",
            password="adminpassword",
            is_verified=True,
        )
        self.stdout.write("Admin user created")
