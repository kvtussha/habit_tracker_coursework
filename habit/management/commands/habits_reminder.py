from django.core.management.base import BaseCommand

from habit.tasks import habits_reminder


class Command(BaseCommand):
    help = 'Run habit reminder task'

    def handle(self, *args, **options):
        habits_reminder()
