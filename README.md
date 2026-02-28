# 🥗 Food Notes

Телеграм-бот для автоматического занесения чеков из Самоката в Google Таблицу.

## Как это работает

Отправляете ссылку на чек с `lk.platformaofd.ru` — бот парсит дату, сумму и продукты и записывает их в таблицу.

<img width="1776" height="643" alt="image" src="https://github.com/user-attachments/assets/51fd1d7d-62a4-4c80-9be3-083ef3c615b3" />

## Стек

- `aiogram 3` — телеграм-бот
- `aiohttp` + `BeautifulSoup` — парсинг чеков
- `gspread` — запись в Google Sheets

## Запуск
```bash
cp .env.example .env
# заполнить .env
cd src && poetry run python main.py
```

## .env
```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_ACCESSED_USERNAMES=
GOOGLE_CREDENTIALS_JSON=
SPREADSHEET_ID=
