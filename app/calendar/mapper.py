from datetime import datetime

from app.payment.models import Lesson


def event_to_lesson(event: dict) -> Lesson | None:
    if "dateTime" not in event["start"]:
        return None
    
    event_id = event["id"]
    title = event.get("summary", "Без названия")
    starts_at = datetime.fromisoformat(event["start"]["dateTime"])
    ends_at = datetime.fromisoformat(event["end"]["dateTime"])

    return Lesson(
        event_id=event_id,
        title=title,
        starts_at=starts_at,
        ends_at=ends_at,
        is_paid=is_event_paid(event),
    )


def events_to_lessons(events: list[dict]) -> list[Lesson]:
    lessons = []

    for event in events:
        lesson = event_to_lesson(event)
        if lesson is not None:
            lessons.append(lesson)

    return lessons


def is_event_paid(event: dict) -> bool:
    return event.get("colorId") == "2"
