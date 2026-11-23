from fitness.exceptions import InvalidValueError
from fitness.exercises.constants import MAX_LEVEL, MIN_LEVEL
from fitness.exercises.exercise import Exercise
from fitness.validation import ensure_number


class BalanceExercise(Exercise):
    """Упражнение на равновесие с уровнем устойчивости опоры."""

    CATEGORY = "баланс"
    SUPPORT_THRESHOLD = 2

    def __init__(self, name, primary_muscle, difficulty, stability_level=MIN_LEVEL, met_value=3.0):
        super().__init__(name, primary_muscle, difficulty, met_value)
        self._stability_level = ensure_number(stability_level, "уровень устойчивости", MIN_LEVEL, MAX_LEVEL)

    @property
    def stability_level(self):
        return self._stability_level

    def progress(self):
        if self._stability_level >= MAX_LEVEL:
            raise InvalidValueError("Достигнут максимальный уровень устойчивости")
        self._stability_level += 1
        return self._stability_level

    def requires_support(self):
        return self._stability_level <= self.SUPPORT_THRESHOLD
