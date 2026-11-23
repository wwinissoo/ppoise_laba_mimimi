from datetime import date, datetime, timedelta

from fitness.exceptions import EntityNotFoundError, InvalidValueError
from fitness.validation import ensure_count, ensure_instance, ensure_text
from fitness.workouts.constants import DAYS_PER_WEEK
from fitness.workouts.workout_template import WorkoutTemplate


class WorkoutPlan:
    """План на несколько недель: шаблон на каждый тренировочный день недели."""

    def __init__(self, name, start_date, weeks):
        self._name = ensure_text(name, "название плана")
        self._start_date = ensure_instance(start_date, date, "дата начала")
        self._weeks = ensure_count(weeks, "недели", minimum=1)
        self._schedule = {}

    @property
    def name(self):
        return self._name

    @property
    def start_date(self):
        return self._start_date

    @property
    def weeks(self):
        return self._weeks

    @property
    def schedule(self):
        return dict(self._schedule)

    def end_date(self):
        return self._start_date + timedelta(days=self._weeks * DAYS_PER_WEEK - 1)

    def assign(self, weekday, template):
        if not isinstance(weekday, int) or not 0 <= weekday < DAYS_PER_WEEK:
            raise InvalidValueError("День недели — число от 0 (пн) до 6 (вс)")
        self._schedule[weekday] = ensure_instance(template, WorkoutTemplate, "шаблон")

    def unassign(self, weekday):
        if weekday not in self._schedule:
            raise EntityNotFoundError(f"На день {weekday} тренировка не назначена")
        del self._schedule[weekday]

    def covers(self, day):
        return self._start_date <= day <= self.end_date()

    def template_for(self, day):
        return self._schedule.get(day.weekday()) if self.covers(day) else None

    def is_rest_day(self, day):
        return self.template_for(day) is None

    def sessions_per_week(self):
        return len(self._schedule)

    def total_sessions(self):
        return self.sessions_per_week() * self._weeks

    def schedule_workout(self, user, day, start_hour=18):
        template = self.template_for(day)
        if template is None:
            raise EntityNotFoundError(f"{day} — день отдыха по плану «{self._name}»")
        return template.instantiate(user, datetime(day.year, day.month, day.day, start_hour))
