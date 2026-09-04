
from datetime import time

from googleapiclient.discovery import build
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from app.bot.handlers import check_payments, daily_payment_check, paid_button, start
from app.calendar.auth import get_credentials
from app.config.settings import ASK_HOUR, MOSCOW_TIMEZONE, TELEGRAM_BOT_TOKEN


def run_bot() -> None:
    credentials = get_credentials()
    calendar_service = build("calendar", "v3", credentials=credentials)

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.bot_data["calendar_service"] = calendar_service

    application.add_handler(CallbackQueryHandler(paid_button, pattern=r"^paid:"))

    application.add_handler(CommandHandler("start", start))

    application.add_handler(
    CommandHandler(
        "check_payments",
        check_payments,
    ))

    job_queue = application.job_queue
    if job_queue is None:
        raise RuntimeError("JobQueue is not available")

    job_queue.run_daily(
        daily_payment_check,
        time=time(
            hour=ASK_HOUR,
            tzinfo=MOSCOW_TIMEZONE,
        ),
    )

    application.run_polling()

if __name__ == "__main__":
    run_bot()