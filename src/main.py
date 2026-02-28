import asyncio

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    from telegram_bot.bot import start_bot
    asyncio.run(start_bot())
