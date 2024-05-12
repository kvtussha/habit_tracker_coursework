from django.utils import timezone
from users.models import User


def check_activity():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)

    for user in inactive_users:
        user.is_active = False
        user.save()
