from datetime import datetime

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import ContextTypes

from app.calendar.client import get_events_for_date, mark_event_as_paid
from app.calendar.mapper import events_to_lessons
from app.config.settings import MOSCOW_TIMEZONE, TELEGRAM_CHAT_ID
from app.payment.service import (
    format_payment_question,
    get_lessons_to_check,
)


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
        reply_markup=keyboard,
        parse_mode="HTML",
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

    calendar_service = context.application.bot_data["calendar_service"]

    mark_event_as_paid(
        calendar_service,
        event_id,
    )

    if not isinstance(query.message, Message):
        return

    text = query.message.text
    if text is None:
        return

    # await query.edit_message_text(
    #     f"✅ {text}"
    # )

    await query.delete_message()


async def check_payments(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    calendar_service = context.application.bot_data["calendar_service"]

    today = datetime.now(MOSCOW_TIMEZONE).date()

    events = get_events_for_date(
        calendar_service,
        today,
    )
    lessons = events_to_lessons(events)

    lessons_to_check = get_lessons_to_check(
        lessons,
        today,
    )

    for lesson in lessons_to_check:
        await send_payment_question(
            bot=context.bot,
            chat_id=TELEGRAM_CHAT_ID,
            lesson=lesson,
        )

async def daily_payment_check(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    calendar_service = context.application.bot_data["calendar_service"]

    today = datetime.now(MOSCOW_TIMEZONE).date()

    events = get_events_for_date(
        calendar_service,
        today,
    )
    lessons = events_to_lessons(events)
    lessons_to_check = get_lessons_to_check(
        lessons,
        today,
    )

    for lesson in lessons_to_check:
        await send_payment_question(
            bot=context.bot,
            chat_id=TELEGRAM_CHAT_ID,
            lesson=lesson,
        )