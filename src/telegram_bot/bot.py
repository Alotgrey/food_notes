import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from telegram_bot.handlers import telegram_router

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command='/start', description='Пройти модерацию'),
    ]
    await bot.set_my_commands(commands)


async def start_bot() -> None:
    logger.warning('Bot is starting...')
    bot = Bot(token=getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(telegram_router)
    await set_commands(bot)
    await dp.start_polling(bot)
