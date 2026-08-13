from datetime import date

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
