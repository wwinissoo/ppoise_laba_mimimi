from datetime import datetime, timedelta

from fitness.tracking.constants import MET_DIVISOR, MET_OXYGEN_FACTOR
from fitness.users.user import User
from fitness.validation import ensure_instance, ensure_positive


class Activity:
    """Базовая активность с длительностью и оценкой калорий по MET."""

    MET = 5.0
    KIND = "активность"

    def __init__(self, user, started_at, duration_minutes):
        self._user = ensure_instance(user, User, "пользователь")
        self._started_at = ensure_instance(started_at, datetime, "начало")
        self._duration_minutes = ensure_positive(duration_minutes, "длительность")

    @property
    def user(self):
        return self._user

    @property
    def started_at(self):
        return self._started_at

    @property
    def duration_minutes(self):
        return self._duration_minutes

    def ends_at(self):
        return self._started_at + timedelta(minutes=self._duration_minutes)

    def overlaps(self, other):
        ensure_instance(other, Activity, "активность")
        return self._started_at < other.ends_at() and other.started_at < self.ends_at()

    def distance_km(self):
        return 0.0

    def calories_burned(self, body_weight_kg):
        ensure_positive(body_weight_kg, "вес")
        return round(self.MET * MET_OXYGEN_FACTOR * body_weight_kg / MET_DIVISOR * self._duration_minutes, 1)

    def summary(self):
        return f"{self.KIND}: {self._duration_minutes} мин, {self.distance_km():.2f} км"
