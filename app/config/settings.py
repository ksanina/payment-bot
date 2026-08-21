from os import getenv
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

MOSCOW_TIMEZONE = ZoneInfo("Europe/Moscow")
ASK_HOUR = 22

load_dotenv()

token = getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env file")

TELEGRAM_BOT_TOKEN = token

chat_id = getenv("TELEGRAM_CHAT_ID")
if not chat_id:
    raise RuntimeError("TELEGRAM_CHAT_ID is not set in .env file")

TELEGRAM_CHAT_ID = int(chat_id)

calendar_id = getenv("GOOGLE_CALENDAR_ID")
if not calendar_id:
    raise RuntimeError("GOOGLE_CALENDAR_ID is not set in .env file")

GOOGLE_CALENDAR_ID = calendar_id