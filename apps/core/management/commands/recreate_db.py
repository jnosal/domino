import os

from django.core.management import BaseCommand, call_command
from django.conf import settings


class Command(BaseCommand):
    """
        Drops sqlite database used for that project.
        Creates new one and applies migrations
    """
    def handle(self, *test_labels, **options):
        database_file = settings.DATABASES['default']['NAME']
        self.stdout.write(u"Dropping database {0}".format(
            database_file
        ))

        try:
            os.remove(database_file)
        except OSError:
            self.stderr.write(u"Error deleting {0}".format(
                database_file
            ))

        self.stdout.write(u"Migrating database")
        call_command('migrate', interactive=True)

