from datetime import date

from fitness.exceptions import InvalidMeasurementError
from fitness.tracking.constants import METERS_PER_KM
from fitness.tracking.sleep_record import SleepRecord
from fitness.validation import ensure_count, ensure_instance, ensure_positive


class DailyActivity:
    """Шаги, активные минуты и этажи за день."""

    def __init__(self, day, step_goal=10_000):
        self._day = ensure_instance(day, date, "день")
        self._step_goal = ensure_count(step_goal, "цель по шагам", minimum=1)
        self._steps = 0
        self._active_minutes = 0
        self._floors = 0
        self._sleep = None

    @property
    def day(self):
        return self._day

    @property
    def step_goal(self):
        return self._step_goal

    @property
    def steps(self):
        return self._steps

    @property
    def active_minutes(self):
        return self._active_minutes

    @property
    def floors(self):
        return self._floors

    @property
    def sleep(self):
        return self._sleep

    def attach_sleep(self, sleep):
        ensure_instance(sleep, SleepRecord, "сон")
        if sleep.woke_up.date() != self._day:
            raise InvalidMeasurementError("Сон должен заканчиваться в день учёта активности")
        self._sleep = sleep

    def is_well_recovered(self):
        return self._sleep is not None and self._sleep.is_sufficient() and self._sleep.quality_label() != "плохой"

    def add_steps(self, steps):
        self._steps += ensure_count(steps, "шаги")
        return self._steps

    def add_active_minutes(self, minutes):
        self._active_minutes += ensure_count(minutes, "активные минуты")
        return self._active_minutes

    def climb_floors(self, floors):
        self._floors += ensure_count(floors, "этажи")
        return self._floors

    def distance_km(self, stride_m=0.75):
        ensure_positive(stride_m, "длина шага")
        return round(self._steps * stride_m / METERS_PER_KM, 2)

    def goal_progress(self):
        return min(100.0, round(self._steps / self._step_goal * 100, 1))

    def is_goal_reached(self):
        return self._steps >= self._step_goal
