from datetime import date, timedelta

from fitness.exceptions import InvalidValueError, WorkoutStateError
from fitness.validation import ensure_instance, ensure_text
from fitness.workouts.workout import Workout


class StreakTracker:
    """Подсчёт серии дней подряд с выполненной активностью."""

    def __init__(self, habit):
        self._habit = ensure_text(habit, "привычка")
        self._current_streak = 0
        self._longest_streak = 0
        self._last_day = None

    @property
    def habit(self):
        return self._habit

    @property
    def current_streak(self):
        return self._current_streak

    @property
    def longest_streak(self):
        return self._longest_streak

    @property
    def last_day(self):
        return self._last_day

    def register(self, day):
        ensure_instance(day, date, "день")
        if self._last_day is not None and day < self._last_day:
            raise InvalidValueError("Нельзя отметить день раньше последней отметки")
        if day == self._last_day:
            return self._current_streak
        consecutive = self._last_day is not None and day - self._last_day == timedelta(days=1)
        self._current_streak = self._current_streak + 1 if consecutive else 1
        self._longest_streak = max(self._longest_streak, self._current_streak)
        self._last_day = day
        return self._current_streak

    def register_workout(self, workout):
        ensure_instance(workout, Workout, "тренировка")
        if workout.status != Workout.COMPLETED:
            raise WorkoutStateError("В серию засчитывается только завершённая тренировка")
        return self.register(workout.finished_at.date())

    def is_broken(self, today):
        return self._last_day is None or (today - self._last_day).days > 1

    def reset(self):
        self._current_streak = 0
        self._last_day = None
