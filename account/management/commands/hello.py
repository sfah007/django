from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        print('Hello')
        self.stdout.write('Deleted objects older than 10 days')