import asyncio
import json
from datetime import datetime
from os import getenv

import gspread
from google.oauth2.service_account import Credentials

CREDS_JSON = getenv('GOOGLE_CREDENTIALS_JSON')
SPREADSHEET_ID = getenv('SPREADSHEET_ID')
SHEET_NAME = getenv('SHEET_NAME')


def _find_row_by_date(sheet, date: datetime) -> int | None:
    """Ищет номер строки по дате в столбце A"""
    date_str = date.strftime('%d/%m/%Y')
    cell = sheet.find(date_str)
    return cell.row if cell else None


def _write_to_sheet(products: str, final_sum: int, date: datetime, ) -> None:
    creds = Credentials.from_service_account_info(
        json.loads(CREDS_JSON),
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    sheet = spreadsheet.worksheet(SHEET_NAME)

    row = _find_row_by_date(sheet, date)
    if row is None:
        raise ValueError(f'Дата {date} не найдена в таблице')

    # D = столбец 4 (Сумма), E = столбец 5 (Продукты)
    sheet.update_cell(row, 4, final_sum)
    sheet.update_cell(row, 5, products)


async def write_cheque_to_sheet(
    products:str,
    final_sum: int,
    date: datetime,
) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        _write_to_sheet,
        products,
        final_sum,
        date,
    )
