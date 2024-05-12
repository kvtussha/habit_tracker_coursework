from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            username='admin_katyssha',
            phone='79603023345',
            bot_id=5121595163,
        )
        user.set_password('admin!#601^?')
        user.is_active = True
        user.save()
