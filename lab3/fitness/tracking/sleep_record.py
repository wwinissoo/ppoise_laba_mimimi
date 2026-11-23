from datetime import datetime

from fitness.exceptions import InvalidMeasurementError
from fitness.tracking.constants import MINUTES_PER_HOUR, SECONDS_PER_HOUR
from fitness.validation import ensure_count, ensure_instance


class SleepRecord:
    """Ночной сон с фазами и пробуждениями."""

    GOOD_EFFICIENCY = 45
    FAIR_EFFICIENCY = 30
    MAX_GOOD_AWAKENINGS = 2

    def __init__(self, went_to_bed, woke_up, deep_minutes, rem_minutes, awakenings=0):
        self._went_to_bed = ensure_instance(went_to_bed, datetime, "отбой")
        self._woke_up = ensure_instance(woke_up, datetime, "подъём")
        if self._woke_up <= self._went_to_bed:
            raise InvalidMeasurementError("Подъём должен быть позже отбоя")
        self._deep_minutes = ensure_count(deep_minutes, "глубокий сон")
        self._rem_minutes = ensure_count(rem_minutes, "REM-сон")
        if self._deep_minutes + self._rem_minutes > self.duration_minutes():
            raise InvalidMeasurementError("Фазы сна длиннее самого сна")
        self._awakenings = ensure_count(awakenings, "пробуждения")

    @property
    def went_to_bed(self):
        return self._went_to_bed

    @property
    def woke_up(self):
        return self._woke_up

    @property
    def deep_minutes(self):
        return self._deep_minutes

    @property
    def rem_minutes(self):
        return self._rem_minutes

    @property
    def awakenings(self):
        return self._awakenings

    def duration_minutes(self):
        return (self._woke_up - self._went_to_bed).total_seconds() / MINUTES_PER_HOUR

    def duration_hours(self):
        return round((self._woke_up - self._went_to_bed).total_seconds() / SECONDS_PER_HOUR, 2)

    def restorative_percent(self):
        return round((self._deep_minutes + self._rem_minutes) / self.duration_minutes() * 100, 1)

    def quality_label(self):
        percent = self.restorative_percent()
        if percent >= self.GOOD_EFFICIENCY and self._awakenings <= self.MAX_GOOD_AWAKENINGS:
            return "отличный"
        if percent >= self.FAIR_EFFICIENCY:
            return "нормальный"
        return "плохой"

    def is_sufficient(self, minimum_hours=7):
        return self.duration_hours() >= minimum_hours
