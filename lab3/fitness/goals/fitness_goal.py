from datetime import date

from fitness.exceptions import GoalStateError, InvalidValueError
from fitness.validation import ensure_instance, ensure_number, ensure_text


class FitnessGoal:
    """Цель с числовым прогрессом и сроком."""

    ACTIVE = "активна"
    ACHIEVED = "достигнута"
    ABANDONED = "отменена"

    def __init__(self, title, start_value, target_value, deadline):
        self._title = ensure_text(title, "название цели")
        self._start_value = ensure_number(start_value, "начальное значение")
        self._target_value = ensure_number(target_value, "целевое значение")
        if self._start_value == self._target_value:
            raise InvalidValueError("Целевое значение должно отличаться от начального")
        self._deadline = ensure_instance(deadline, date, "срок")
        self._current_value = self._start_value
        self._status = self.ACTIVE

    @property
    def title(self):
        return self._title

    @property
    def start_value(self):
        return self._start_value

    @property
    def target_value(self):
        return self._target_value

    @property
    def deadline(self):
        return self._deadline

    @property
    def current_value(self):
        return self._current_value

    @property
    def status(self):
        return self._status

    def _require_active(self):
        if self._status != self.ACTIVE:
            raise GoalStateError(f"Цель «{self._title}» уже {self._status}")

    def update_progress(self, value):
        self._require_active()
        self._current_value = ensure_number(value, "текущее значение")
        if self.progress_percent() >= 100:
            self._status = self.ACHIEVED
        return self._status

    def progress_percent(self):
        done = (self._current_value - self._start_value) / (self._target_value - self._start_value) * 100
        return round(min(100.0, max(0.0, done)), 1)

    def is_achieved(self):
        return self._status == self.ACHIEVED

    def days_left(self, today):
        return (self._deadline - today).days

    def is_overdue(self, today):
        return self._status == self.ACTIVE and today > self._deadline

    def abandon(self):
        self._require_active()
        self._status = self.ABANDONED
