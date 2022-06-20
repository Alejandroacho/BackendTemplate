from django.core.management.base import BaseCommand
from django.db import connection


GRANT: str = 'grant all privileges on *.* to "admin"@"%" with grant option;'
CREATE: str = "create database if not exists test_database;"


class Command(BaseCommand):

    help: str = "Creates the testing database"

    def handle(self, *args: tuple, **options: dict) -> None:
        self.execute_sql()

    def execute_sql(self) -> None:
        with connection.cursor() as cursor:
            cursor.execute(GRANT)
            cursor.execute(CREATE)
