from fitness.exercises.exercise import Exercise
from fitness.validation import ensure_count, ensure_instance, ensure_number
from fitness.workouts.constants import SECONDS_PER_MINUTE, SECONDS_PER_REP
from fitness.workouts.exercise_set import ExerciseSet
from fitness.workouts.workout_entry import WorkoutEntry


class TemplateItem:
    """Пункт шаблона: упражнение и целевые подходы/повторения/вес."""

    def __init__(self, exercise, target_sets, target_reps, target_weight_kg=0, rest_seconds=90):
        self._exercise = ensure_instance(exercise, Exercise, "упражнение")
        self._target_sets = ensure_count(target_sets, "подходы", minimum=1)
        self._target_reps = ensure_count(target_reps, "повторения", minimum=1)
        self._target_weight_kg = ensure_number(target_weight_kg, "вес", minimum=0)
        self._rest_seconds = ensure_number(rest_seconds, "отдых", minimum=0)

    @property
    def exercise(self):
        return self._exercise

    @property
    def target_sets(self):
        return self._target_sets

    @property
    def target_reps(self):
        return self._target_reps

    @property
    def target_weight_kg(self):
        return self._target_weight_kg

    @property
    def rest_seconds(self):
        return self._rest_seconds

    def estimated_minutes(self):
        work = self._target_sets * self._target_reps * SECONDS_PER_REP
        rest = (self._target_sets - 1) * self._rest_seconds
        return round((work + rest) / SECONDS_PER_MINUTE, 1)

    def planned_volume(self):
        return self._target_sets * self._target_reps * self._target_weight_kg

    def to_entry(self):
        entry = WorkoutEntry(self._exercise, note="по шаблону")
        for _ in range(self._target_sets):
            entry.add_set(ExerciseSet(self._target_reps, self._target_weight_kg))
        return entry
