from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from app.payment.models import Lesson
from app.payment.service import format_payment_question, get_lessons_to_check

MOSCOW_TIMEZONE = ZoneInfo("Europe/Moscow")

def test_get_lessons_to_check():
    today = date(2026, 8, 11)
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    lessons = [
        Lesson(
            event_id='1',
            title='Вика',
            starts_at=datetime.combine(today, time(11, 0), tzinfo=MOSCOW_TIMEZONE),
            ends_at=datetime.combine(today, time(12, 0), tzinfo=MOSCOW_TIMEZONE),
            is_paid=False
        ),
        Lesson(
            event_id='2',
            title='Вика',
            starts_at=datetime.combine(today, time(11, 0), tzinfo=MOSCOW_TIMEZONE),
            ends_at=datetime.combine(today, time(12, 0), tzinfo=MOSCOW_TIMEZONE),
            is_paid=True
        ),
        Lesson(
            event_id='3',
            title='Вика',
            starts_at=datetime.combine(tomorrow, time(11, 0), tzinfo=MOSCOW_TIMEZONE),
            ends_at=datetime.combine(tomorrow, time(12, 0), tzinfo=MOSCOW_TIMEZONE),
            is_paid=False
        ),
        Lesson(
            event_id='4',
            title='Вика',
            starts_at=datetime.combine(yesterday, time(11, 0), tzinfo=MOSCOW_TIMEZONE),
            ends_at=datetime.combine(yesterday, time(12, 0), tzinfo=MOSCOW_TIMEZONE),
            is_paid=False
        ),
    ]

    lessons_to_check = get_lessons_to_check(lessons, today)
    lessons_to_check_ids = [lesson.event_id for lesson in lessons_to_check]

    assert lessons_to_check_ids == ["1"]

def test_format_payment_question():
    lesson = Lesson(
        event_id='1',
        title='Вика',
        starts_at=datetime(2026, 8, 11, 11, 0, tzinfo=MOSCOW_TIMEZONE),
        ends_at=datetime(2026, 8, 11, 12, 0, tzinfo=MOSCOW_TIMEZONE),
        is_paid=False
    )

    question = format_payment_question(lesson)

    assert question == (
        "<b>Вика</b> | 11:00 — 12:00"
    )