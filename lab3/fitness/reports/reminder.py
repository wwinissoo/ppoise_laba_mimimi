from datetime import datetime, time, timedelta

from fitness.exceptions import ScheduleConflictError
from fitness.reports.constants import DAYS_PER_WEEK
from fitness.validation import ensure_instance, ensure_text


class Reminder:
    """Повторяющееся напоминание в заданное время по дням недели."""

    def __init__(self, message, remind_at, weekdays):
        self._message = ensure_text(message, "текст напоминания")
        self._remind_at = ensure_instance(remind_at, time, "время напоминания")
        self._weekdays = frozenset(weekdays)
        if not self._weekdays or not self._weekdays <= set(range(DAYS_PER_WEEK)):
            raise ScheduleConflictError("Дни недели — непустой набор чисел 0..6")
        self._active = True
        self._last_fired_on = None

    @property
    def message(self):
        return self._message

    @property
    def remind_at(self):
        return self._remind_at

    @property
    def weekdays(self):
        return tuple(sorted(self._weekdays))

    @property
    def active(self):
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def clashes_with(self, other):
        return self._remind_at == other.remind_at and bool(self._weekdays & set(other.weekdays))

    def is_due(self, now):
        return (
            self._active
            and now.weekday() in self._weekdays
            and now.time() >= self._remind_at
            and self._last_fired_on != now.date()
        )

    def mark_fired(self, now):
        self._last_fired_on = now.date()

    def next_occurrence(self, now):
        for offset in range(DAYS_PER_WEEK + 1):
            day = now.date() + timedelta(days=offset)
            moment = datetime.combine(day, self._remind_at)
            if day.weekday() in self._weekdays and moment > now:
                return moment
        return None
