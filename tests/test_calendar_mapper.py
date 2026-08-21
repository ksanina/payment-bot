from datetime import datetime

from app.calendar.mapper import event_to_lesson, events_to_lessons, is_event_paid


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

