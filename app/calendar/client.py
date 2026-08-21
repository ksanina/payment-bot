from datetime import date, datetime, time, timedelta

from app.config.settings import GOOGLE_CALENDAR_ID, MOSCOW_TIMEZONE


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
            calendarId=GOOGLE_CALENDAR_ID,
            timeMin=start_of_day.isoformat(),
            timeMax=start_of_next_day.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
    )

    return request.execute().get("items", [])