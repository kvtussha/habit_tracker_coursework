from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            username='katerina_admin',
            phone='79603023345',
            bot_id=5121595186,
            is_superuser=True,
            is_staff=True
        )
        user.set_password('katya_admin_')
        user.save()
