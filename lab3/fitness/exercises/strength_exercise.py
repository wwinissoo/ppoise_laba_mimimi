from fitness.exceptions import InvalidValueError
from fitness.exercises.exercise import Exercise
from fitness.validation import ensure_count, ensure_number


class StrengthExercise(Exercise):
    """Силовое упражнение с отягощением."""

    CATEGORY = "силовое"
    EPLEY_DIVISOR = 30
    COMPOUND_REST_SECONDS = 180
    ISOLATION_REST_SECONDS = 90

    def __init__(
        self, name, primary_muscle, difficulty, met_value=6.0, equipment=(), secondary_muscles=(), compound=False
    ):
        super().__init__(name, primary_muscle, difficulty, met_value, equipment, secondary_muscles)
        self._compound = bool(compound)

    @property
    def compound(self):
        return self._compound

    def estimate_one_rep_max(self, weight_kg, reps):
        """Формула Эпли: вес × (1 + повторы / 30)."""
        ensure_number(weight_kg, "вес снаряда", minimum=0)
        ensure_count(reps, "повторения", minimum=1)
        if reps == 1:
            return float(weight_kg)
        return round(weight_kg * (1 + reps / self.EPLEY_DIVISOR), 1)

    def recommended_rest_seconds(self):
        return self.COMPOUND_REST_SECONDS if self._compound else self.ISOLATION_REST_SECONDS

    def check_load(self, weight_kg):
        overloaded = [item.name for item in self._equipment if not item.can_handle(weight_kg)]
        if overloaded:
            raise InvalidValueError(f"Вес {weight_kg} кг недопустим для: {', '.join(overloaded)}")
        return True
