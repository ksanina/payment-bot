from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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

def get_today_events(service) -> list[dict]:
    now = datetime.now(MOSCOW_TIMEZONE)

    start_of_day = datetime.combine(
        now.date(),
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

def format_event(event: dict) -> str:
    title = event.get("summary", "Без названия")

    start = event["start"].get(
        "dateTime",
        event["start"].get("date"),
    )

    end = event["end"].get(
        "dateTime",
        event["end"].get("date"),
    )

    start_time = datetime.fromisoformat(start).strftime("%H:%M")
    end_time = datetime.fromisoformat(end).strftime("%H:%M")

    return f"{title}: {start_time} — {end_time}"

def print_events(events: list[dict]) -> None:
    if not events:
        print("На сегодня уроков нет.")
        return

    for event in events:
        print(format_event(event))

credentials = get_credentials()
service = build("calendar", "v3", credentials=credentials)
events = get_today_events(service)
print_events(events)
