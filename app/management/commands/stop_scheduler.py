from django.core.management.base import BaseCommand
from app.scheduler import stop_scheduler


class Command(BaseCommand):
    help = 'Stop the APScheduler'

    def handle(self, *args, **options):
        stop_scheduler()
        self.stdout.write(self.style.SUCCESS('APScheduler stopped'))
