import os
import asyncio
from datetime import timedelta

import aiohttp
import logging
from celery import shared_task
from django.utils import timezone
from habit.models import Habit

logger = logging.getLogger(__name__)


@shared_task
def habits_reminder():
    asyncio.run(send_habit_reminders())


async def send_habit_reminders():
    url = 'https://api.telegram.org/bot'
    token = os.getenv('TELEGRAM_TOKEN')

    if not token:
        logger.error('TELEGRAM_TOKEN is not set')
        return

    time_now = timezone.now().time().replace(second=0, microsecond=0)
    date_now = timezone.now().date()
    habits_to_send = Habit.objects.filter(is_pleasant_habit='Нет')

    async with aiohttp.ClientSession() as session:
        tasks = []
        for habit in habits_to_send:
            if habit.time == time_now:
                chat_id = habit.user.bot_id
                text = f"Вам нужно {habit.action} в {habit.time} в {habit.place}"
                task = send_message(session, url, token, chat_id, text)
                tasks.append(task)

                # Обновляем дату выполнения привычки
                habit.date = date_now + timedelta(days=habit.frequency)
                habit.save()

        await asyncio.gather(*tasks)


async def send_message(session, url, token, chat_id, text):
    try:
        async with session.post(
                url=f"{url}{token}/sendMessage",
                data={
                    "chat_id": chat_id,
                    "text": text
                }
        ) as response:
            response.raise_for_status()
            logger.info(f'Message sent to {chat_id}: {text}')
    except aiohttp.ClientError as e:
        logger.error(f'Failed to send message to {chat_id}: {e}')
