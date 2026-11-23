from fitness.exceptions import InvalidValueError
from fitness.exercises.strength_exercise import StrengthExercise
from fitness.goals.fitness_goal import FitnessGoal
from fitness.validation import ensure_instance
from fitness.workouts.exercise_set import ExerciseSet


class StrengthGoal(FitnessGoal):
    """Цель по разовому максимуму в силовом упражнении."""

    def __init__(self, exercise, current_one_rep_max, target_one_rep_max, deadline):
        self._exercise = ensure_instance(exercise, StrengthExercise, "силовое упражнение")
        super().__init__(f"1ПМ: {exercise.name}", current_one_rep_max, target_one_rep_max, deadline)

    @property
    def exercise(self):
        return self._exercise

    def record_set(self, exercise, exercise_set):
        ensure_instance(exercise_set, ExerciseSet, "подход")
        if exercise is not self._exercise:
            raise InvalidValueError(f"Цель отслеживает только «{self._exercise.name}»")
        if not exercise_set.completed or exercise_set.reps == 0:
            return self.status
        estimate = self._exercise.estimate_one_rep_max(exercise_set.weight_kg, exercise_set.reps)
        return self.update_progress(estimate) if estimate > self.current_value else self.status
