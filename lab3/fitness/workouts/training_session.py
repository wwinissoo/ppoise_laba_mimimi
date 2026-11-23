from datetime import datetime, timedelta

from fitness.exceptions import ScheduleConflictError, WorkoutStateError
from fitness.users.trainer import Trainer
from fitness.users.user import User
from fitness.validation import ensure_instance, ensure_positive


class TrainingSession:
    """Запись клиента на персональную тренировку."""

    BOOKED = "забронирована"
    DONE = "проведена"
    CANCELLED = "отменена"
    LATE_CANCEL_HOURS = 24
    LATE_CANCEL_PENALTY = 0.5

    def __init__(self, trainer, client, starts_at, duration_minutes=60):
        self._trainer = ensure_instance(trainer, Trainer, "тренер")
        self._client = ensure_instance(client, User, "клиент")
        self._starts_at = ensure_instance(starts_at, datetime, "начало")
        self._duration_minutes = ensure_positive(duration_minutes, "длительность")
        self._status = self.BOOKED

    @property
    def trainer(self):
        return self._trainer

    @property
    def client(self):
        return self._client

    @property
    def starts_at(self):
        return self._starts_at

    @property
    def duration_minutes(self):
        return self._duration_minutes

    @property
    def status(self):
        return self._status

    def ends_at(self):
        return self._starts_at + timedelta(minutes=self._duration_minutes)

    def fee(self):
        return self._trainer.session_fee(self._duration_minutes)

    def overlaps(self, other):
        ensure_instance(other, TrainingSession, "сессия")
        same_people = other.trainer is self._trainer or other.client is self._client
        return same_people and self._starts_at < other.ends_at() and other.starts_at < self.ends_at()

    def _require_booked(self):
        if self._status != self.BOOKED:
            raise WorkoutStateError(f"Сессия уже {self._status}")

    def reschedule(self, new_start, other_sessions=()):
        self._require_booked()
        original = self._starts_at
        self._starts_at = ensure_instance(new_start, datetime, "новое начало")
        if any(item is not self and item.status == self.BOOKED and self.overlaps(item) for item in other_sessions):
            self._starts_at = original
            raise ScheduleConflictError("Новое время пересекается с другой сессией")

    def complete(self):
        self._require_booked()
        self._status = self.DONE

    def cancel(self, now):
        """Отменяет сессию и возвращает штраф за позднюю отмену."""
        self._require_booked()
        self._status = self.CANCELLED
        if self._starts_at - now < timedelta(hours=self.LATE_CANCEL_HOURS):
            return round(self.fee() * self.LATE_CANCEL_PENALTY, 2)
        return 0
