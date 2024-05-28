# habit/management/commands/start_celery.py
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start Celery worker and beat'

    def handle(self, *args, **options):
        celery_worker_command = ['celery', '-A', 'config', 'worker', '-B', '--loglevel=info']

        self.stdout.write(self.style.SUCCESS('Starting Celery worker and beat...'))

        try:
            # Запуск команды Celery worker и beat
            subprocess.run(celery_worker_command, check=True)
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Error starting Celery: {e}'))
