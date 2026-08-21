from datetime import datetime

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.config.settings import MOSCOW_TIMEZONE, TELEGRAM_CHAT_ID
from app.payment.models import Lesson
from app.payment.service import format_payment_question


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text("Бот работает")

async def send_payment_question(
    bot: Bot,
    chat_id: int,
    lesson: Lesson,
) -> None:

    text = format_payment_question(lesson)

    button = InlineKeyboardButton(
        text="Оплачено",
        callback_data=f"paid:{lesson.event_id}",
    )

    keyboard = InlineKeyboardMarkup([[button]])

    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text,
        reply_markup=keyboard
        )

async def test_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    lesson = Lesson(
        event_id="test_event_id",
        title="Тестовый урок",
        starts_at=datetime(2026, 8, 21, 10, 0, tzinfo=MOSCOW_TIMEZONE),
        ends_at=datetime(2026, 8, 21, 11, 0, tzinfo=MOSCOW_TIMEZONE),
        is_paid=False,
    )

    await send_payment_question(
        bot=context.bot,
        chat_id=update.message.chat_id,
        lesson=lesson,
    )

async def paid_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if query is None:
        return

    if query.data is None:
        return

    event_id = query.data.split(":", 1)[1]

    await query.answer()
    print(event_id)