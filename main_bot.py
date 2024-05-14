import asyncio
import logging
import sys

import django

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import router
from config.settings import TELEGRAM_TOKEN

django.setup()

dp = Dispatcher()
bot = Bot(TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
