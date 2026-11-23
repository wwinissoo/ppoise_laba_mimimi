from fitness.exceptions import EntityNotFoundError
from fitness.exercises.exercise import Exercise
from fitness.exercises.strength_exercise import StrengthExercise
from fitness.validation import ensure_instance
from fitness.workouts.exercise_set import ExerciseSet


class WorkoutEntry:
    """Упражнение в тренировке со списком подходов."""

    def __init__(self, exercise, note=""):
        self._exercise = ensure_instance(exercise, Exercise, "упражнение")
        self._note = note.strip() if isinstance(note, str) else ""
        self._sets = []

    @property
    def exercise(self):
        return self._exercise

    @property
    def note(self):
        return self._note

    @property
    def sets(self):
        return tuple(self._sets)

    def add_set(self, exercise_set):
        ensure_instance(exercise_set, ExerciseSet, "подход")
        if isinstance(self._exercise, StrengthExercise):
            self._exercise.check_load(exercise_set.weight_kg)
        self._sets.append(exercise_set)
        return exercise_set

    def remove_set(self, index):
        if not isinstance(index, int) or not 0 <= index < len(self._sets):
            raise EntityNotFoundError(f"Подход №{index} не найден")
        return self._sets.pop(index)

    def completed_sets(self):
        return [item for item in self._sets if item.completed]

    def total_volume(self):
        return sum(item.volume() for item in self.completed_sets())

    def total_duration_seconds(self):
        return sum(item.duration_seconds for item in self.completed_sets())

    def best_set(self):
        completed = self.completed_sets()
        return max(completed, key=lambda item: (item.weight_kg, item.reps)) if completed else None

    def estimated_one_rep_max(self):
        best = self.best_set()
        if best is None or not isinstance(self._exercise, StrengthExercise) or best.reps == 0:
            return 0.0
        return self._exercise.estimate_one_rep_max(best.weight_kg, best.reps)
