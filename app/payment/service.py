from datetime import date
from html import escape

from app.payment.models import Lesson


def get_lessons_to_check(
    lessons: list[Lesson],
    target_date: date,
) -> list[Lesson]:
    lessons_to_check = []

    for lesson in lessons:
        if lesson.starts_at.date() == target_date and not lesson.is_paid:
            lessons_to_check.append(lesson)

    return lessons_to_check

def format_payment_question(lesson: Lesson) -> str:
    return (
        f"<b>{escape(lesson.title)}</b> | "
        f"{lesson.starts_at.strftime('%H:%M')} — {lesson.ends_at.strftime('%H:%M')}"
    )
