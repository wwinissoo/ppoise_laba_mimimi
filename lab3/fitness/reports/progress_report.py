from collections import Counter
from datetime import date

from fitness.exceptions import InvalidValueError
from fitness.reports.constants import DAYS_PER_WEEK
from fitness.users.user import User
from fitness.validation import ensure_instance
from fitness.workouts.workout import Workout


class ProgressReport:
    """Сводка по завершённым тренировкам пользователя за период."""

    def __init__(self, user, period_start, period_end, workouts):
        self._user = ensure_instance(user, User, "пользователь")
        self._period_start = ensure_instance(period_start, date, "начало периода")
        self._period_end = ensure_instance(period_end, date, "конец периода")
        if self._period_end < self._period_start:
            raise InvalidValueError("Конец периода раньше начала")
        self._workouts = [self._check(workout) for workout in workouts if self._in_period(workout)]

    def _check(self, workout):
        if workout.user is not self._user:
            raise InvalidValueError("Отчёт строится только по тренировкам одного пользователя")
        return workout

    def _in_period(self, workout):
        ensure_instance(workout, Workout, "тренировка")
        return (
            workout.status == Workout.COMPLETED and self._period_start <= workout.started_at.date() <= self._period_end
        )

    @property
    def user(self):
        return self._user

    @property
    def period_start(self):
        return self._period_start

    @property
    def period_end(self):
        return self._period_end

    @property
    def workouts(self):
        return tuple(self._workouts)

    def workouts_count(self):
        return len(self._workouts)

    def total_volume(self):
        return sum(workout.total_volume() for workout in self._workouts)

    def average_duration(self):
        if not self._workouts:
            return 0
        return round(sum(workout.duration_minutes() for workout in self._workouts) / len(self._workouts))

    def most_trained_muscle(self):
        counter = Counter(muscle.name for workout in self._workouts for muscle in workout.muscles_worked())
        return counter.most_common(1)[0][0] if counter else None

    def weeks_in_period(self):
        return max(1, ((self._period_end - self._period_start).days + 1) / DAYS_PER_WEEK)

    def consistency_percent(self):
        planned = self._user.settings.weekly_workout_target * self.weeks_in_period()
        return round(min(100.0, self.workouts_count() / planned * 100), 1)

    def summary(self):
        return (
            f"{self._user.username}: {self.workouts_count()} тренировок, объём {self.total_volume()} кг, "
            f"в среднем {self.average_duration()} мин, регулярность {self.consistency_percent()}%"
        )
