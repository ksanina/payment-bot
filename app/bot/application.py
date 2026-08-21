from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from app.bot.handlers import paid_button, start, test_payment
from app.config.settings import TELEGRAM_BOT_TOKEN


def run_bot() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CallbackQueryHandler(paid_button, pattern=r"^paid:"))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test_payment", test_payment))

    application.run_polling()

if __name__ == "__main__":
    run_bot()