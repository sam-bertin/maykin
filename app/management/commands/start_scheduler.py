from django.core.management.base import BaseCommand
from app.scheduler import start_scheduler


class Command(BaseCommand):
    help = 'Start the APScheduler'

    def handle(self, *args, **options):
        start_scheduler()
        self.stdout.write(self.style.SUCCESS('APScheduler started'))
