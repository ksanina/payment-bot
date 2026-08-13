from datetime import datetime

from googleapiclient.discovery import build

from app.calendar.list_events import (
    MOSCOW_TIMEZONE,
    events_to_lessons,
    get_credentials,
    get_events_for_date,
)
from app.payment.service import get_lessons_to_check


def main() -> None:
    credentials = get_credentials()
    service = build("calendar", "v3", credentials=credentials)

    today = datetime.now(MOSCOW_TIMEZONE).date()

    events = get_events_for_date(service, today)
    lessons = events_to_lessons(events)
    lessons_to_check = get_lessons_to_check(
        lessons,
        today,
    )

    print(lessons_to_check)


if __name__ == "__main__":
    main()
