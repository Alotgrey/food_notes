import logging
from os import getenv

from aiogram import Router, types, F
from aiogram.filters import (
    CommandStart,
)

from utils.crud import write_cheque_to_sheet
from utils.parsing import parse_cheque

telegram_router = Router()

accessed = getenv('TELEGRAM_ACCESSED_USERNAMES').split(',')

logger = logging.getLogger(__name__)


def has_access(username: str) -> bool:
    return username in accessed


@telegram_router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    if not has_access(message.from_user.username):
        await message.answer('Нет доступа')
        return
    await message.answer('Привет! Отправь ссылку на чек с platformaofd.ru')


@telegram_router.message(F.text.contains('https://lk.platformaofd.ru'))
async def handle_cheque_link(message: types.Message) -> None:
    if not has_access(message.from_user.username):
        await message.answer('Нет доступа')
        return

    url = message.text.strip()

    try:
        products, final_sum, receipt_date = await parse_cheque(url)
    except Exception as err:
        logger.error(f'Parsing error: {err}')
        await message.answer('Что-то пошло не так при парсинге чека')
        return

    try:
        await write_cheque_to_sheet(products, final_sum, receipt_date)
    except Exception as err:
        logger.error(f'Writing to table error: {err}')
        await message.answer('Что-то пошло не так при добавлении в таблицу')
        return

    await message.answer(f'В таблицу добавлены продукты на сумму {final_sum}р')


@telegram_router.message()
async def handle_unknown(message: types.Message) -> None:
    if not has_access(message.from_user.username):
        await message.answer('Нет доступа')
        return
    await message.answer('Это не чек platformaofd')
