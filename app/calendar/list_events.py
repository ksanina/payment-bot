from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from app.payment.models import Lesson

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
]

MOSCOW_TIMEZONE = ZoneInfo("Europe/Moscow")
CALENDAR_ID = "gnog94n7jvjnq15ha5dktnks7c@group.calendar.google.com"


def get_credentials() -> Credentials:
    if TOKEN_FILE.exists():
        return Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES,
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE,
        SCOPES,
    )
    credentials = flow.run_local_server(port=0)
    TOKEN_FILE.write_text(credentials.to_json())

    return credentials


def get_events_for_date(
    service,
    target_date: date,
) -> list[dict]:
    start_of_day = datetime.combine(
        target_date,
        time.min,
        tzinfo=MOSCOW_TIMEZONE,
    )

    start_of_next_day = start_of_day + timedelta(days=1)

    request = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=start_of_day.isoformat(),
            timeMax=start_of_next_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
    )

    return request.execute().get("items", [])


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
