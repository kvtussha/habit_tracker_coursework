import os

import django

import asyncio
import logging
import sys
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers.authorization import user_router
from bot.handlers.create_habit import create_habit_router
from bot.handlers.delete_habit import delete_habit_router
from bot.handlers.get_habits import get_habits_router
from bot.handlers.update_habit import update_habit_router
from config.settings import TELEGRAM_TOKEN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

dp = Dispatcher()
bot = Bot(TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    dp.include_router(user_router)
    dp.include_router(get_habits_router)
    dp.include_router(create_habit_router)
    dp.include_router(delete_habit_router)
    dp.include_router(update_habit_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
