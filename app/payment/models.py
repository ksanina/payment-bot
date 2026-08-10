# app/payment/models.py

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lesson:
    event_id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    is_paid: bool
