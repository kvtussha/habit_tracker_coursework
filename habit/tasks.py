import os
import logging
import requests
from celery import shared_task
from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def habits_reminder(obj):
    telegram_chat_id = User.objects.get(id=obj["user"]).bot_id
    message = (
        f"Вы запланировали привычку [{obj['action']}]! в [{obj['time']}] в [{obj['place']}], "
        f"[{obj['frequency']}] раз в неделю! "
        f"Вознаграждение [{obj['reward']}]")
    requests.get(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage?chat_id={telegram_chat_id}&"
                 f"text={message}")
