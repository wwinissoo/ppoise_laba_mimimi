from datetime import datetime

from fitness.exceptions import WorkoutStateError
from fitness.users.user import User
from fitness.validation import ensure_instance, ensure_text
from fitness.workouts.constants import SECONDS_PER_MINUTE
from fitness.workouts.workout_entry import WorkoutEntry


class Workout:
    """Тренировка пользователя, состоящая из записей упражнений."""

    PLANNED = "запланирована"
    IN_PROGRESS = "идёт"
    COMPLETED = "завершена"
    CANCELLED = "отменена"
    TRANSITIONS = {
        PLANNED: {IN_PROGRESS, CANCELLED},
        IN_PROGRESS: {COMPLETED, CANCELLED},
        COMPLETED: set(),
        CANCELLED: set(),
    }

    def __init__(self, title, user, planned_start):
        self._title = ensure_text(title, "название тренировки")
        self._user = ensure_instance(user, User, "пользователь")
        self._planned_start = ensure_instance(planned_start, datetime, "плановое начало")
        self._status = self.PLANNED
        self._entries = []
        self._started_at = None
        self._finished_at = None

    @property
    def title(self):
        return self._title

    @property
    def user(self):
        return self._user

    @property
    def planned_start(self):
        return self._planned_start

    @property
    def status(self):
        return self._status

    @property
    def entries(self):
        return tuple(self._entries)

    @property
    def started_at(self):
        return self._started_at

    @property
    def finished_at(self):
        return self._finished_at

    def _move_to(self, target):
        if target not in self.TRANSITIONS[self._status]:
            raise WorkoutStateError(f"Нельзя перевести тренировку из «{self._status}» в «{target}»")
        self._status = target

    def add_entry(self, entry):
        ensure_instance(entry, WorkoutEntry, "запись упражнения")
        if self._status not in (self.PLANNED, self.IN_PROGRESS):
            raise WorkoutStateError("В завершённую или отменённую тренировку нельзя добавлять упражнения")
        self._user.health_profile.check_exercise_allowed(entry.exercise)
        self._entries.append(entry)
        return entry

    def find_entry(self, exercise_name):
        for entry in self._entries:
            if entry.exercise.name.casefold() == exercise_name.strip().casefold():
                return entry
        return None

    def start(self, now):
        if not self._entries:
            raise WorkoutStateError("Нельзя начать пустую тренировку")
        self._move_to(self.IN_PROGRESS)
        self._started_at = ensure_instance(now, datetime, "время начала")

    def finish(self, now):
        ensure_instance(now, datetime, "время окончания")
        if self._status == self.IN_PROGRESS and now < self._started_at:
            raise WorkoutStateError("Окончание не может быть раньше начала")
        if not any(entry.completed_sets() for entry in self._entries):
            raise WorkoutStateError("Нельзя завершить тренировку без выполненных подходов")
        self._move_to(self.COMPLETED)
        self._finished_at = now

    def cancel(self):
        self._move_to(self.CANCELLED)

    def duration_minutes(self):
        if self._started_at is None or self._finished_at is None:
            return 0
        return round((self._finished_at - self._started_at).total_seconds() / SECONDS_PER_MINUTE)

    def total_volume(self):
        return sum(entry.total_volume() for entry in self._entries)

    def completed_sets_count(self):
        return sum(len(entry.completed_sets()) for entry in self._entries)

    def muscles_worked(self):
        return {
            muscle for entry in self._entries if entry.completed_sets() for muscle in entry.exercise.involved_muscles()
        }

    def estimate_calories(self, body_weight_kg):
        """Калории по MET каждого упражнения пропорционально числу выполненных подходов."""
        total_sets = self.completed_sets_count()
        if total_sets == 0:
            return 0.0
        minutes = self.duration_minutes()
        calories = sum(
            entry.exercise.calories_burned(body_weight_kg, minutes * len(entry.completed_sets()) / total_sets)
            for entry in self._entries
        )
        return round(calories, 1)
