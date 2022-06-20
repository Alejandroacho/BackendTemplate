from django.core.management.base import BaseCommand
from django.db import connection


GRANT = 'grant all privileges on *.* to "admin"@"%" with grant option;'
CREATE = 'create database if not exists test_database;'


class Command(BaseCommand):

    help = 'Creates the testing database'

    def handle(self, *args, **options):
        self.execute_sql()

    def execute_sql(self):
        with connection.cursor() as cursor:
            cursor.execute(GRANT)
            cursor.execute(CREATE)
