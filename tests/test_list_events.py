from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from app.calendar.list_events import (
    event_to_lesson,
    events_to_lessons,
    is_event_paid,
)
from app.payment.models import Lesson
from app.payment.service import get_lessons_to_check

MOSCOW_TIMEZONE = ZoneInfo("Europe/Moscow")


def test_event_to_lesson():
    event = {
        "id": "event-123",
        "summary": "Math lesson",
        "start": {
            "dateTime": "2026-08-10T15:15:00+03:00",
        },
        "end": {
            "dateTime": "2026-08-10T17:00:00+03:00",
        },
        "colorId": "2",
    }

    lesson = event_to_lesson(event)

    assert lesson is not None

    assert lesson.event_id == "event-123"
    assert lesson.title == "Math lesson"
    assert lesson.starts_at == datetime.fromisoformat("2026-08-10T15:15:00+03:00")
    assert lesson.ends_at == datetime.fromisoformat("2026-08-10T17:00:00+03:00")
    assert lesson.is_paid is True

def test_event_to_lesson_without_summary():
    event = {
        "id": "event-456",
        "start": {
            "dateTime": "2026-08-10T15:15:00+03:00",
        },
        "end": {
            "dateTime": "2026-08-10T17:00:00+03:00",
        },
    }

    lesson = event_to_lesson(event)

    assert lesson is not None

    assert lesson.event_id == "event-456"
    assert lesson.title == "Без названия"
    assert lesson.starts_at == datetime.fromisoformat("2026-08-10T15:15:00+03:00")
    assert lesson.ends_at == datetime.fromisoformat("2026-08-10T17:00:00+03:00")
    assert lesson.is_paid is False

def test_event_to_lesson_rejects_all_day_event():
    event = {
        "id": "event-123",
        "summary": "Math lesson",
        "start": {
            "date": "2026-08-10",
        },
        "end": {
            "date": "2026-08-11",
        },
    }

    lesson = event_to_lesson(event)

    assert lesson is None

def test_events_to_lessons_skip_all_day_events():
    events = [
        {
            "id": "event-123",
            "summary": "Math lesson",
            "start": {
                "dateTime": "2026-08-10T15:15:00+03:00",
            },
            "end": {
                "dateTime": "2026-08-10T17:00:00+03:00",
            },
        },
        {
            "id": "event-456",
            "summary": "All-day event",
            "start": {
                "date": "2026-08-10",
            },
            "end": {
                "date": "2026-08-11",
            },
        },
    ]

    lessons = events_to_lessons(events)

    assert len(lessons) == 1
    assert lessons[0].event_id == "event-123"

def test_is_event_paid_returns_true_for_paid_color():
    event = {"colorId": "2"}

    assert is_event_paid(event) is True

def test_is_event_paid_returns_false_without_paid_color():
    events = [{"colorId": "1"}, {"colorId": None}, {}]

    for event in events:
        assert is_event_paid(event) is False

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
