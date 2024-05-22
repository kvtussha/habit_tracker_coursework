import os
from datetime import datetime, date, timedelta
import requests
from celery import shared_task

from habit.models import Habit


@shared_task
def habits_reminder():
    url = 'https://api.telegram.org/bot'
    token = os.getenv('TELEGRAM_TOKEN')

    time_now = datetime.now().time().replace(second=0, microsecond=0)
    date_now = date.today()
    habits_to_send = Habit.objects.filter(is_pleasant_habit=False)

    for habit in habits_to_send:
        if habit.time_to_complete == date_now or not habit.date:
            if habit.time_to_complete >= time_now:
                chat_id = habit.user.bot_id
                text = f"Вам нужно {habit.action} в {habit.time_to_complete} в {habit.place}"
                requests.post(
                    url=f"{url}{token}/sendMessage",
                    data={
                        "chat_id": chat_id,
                        "text": text
                    }
                )
            habit.date = date_now + timedelta(days=habit.periodicity)
            habit.save()
