from fitness.exercises.exercise import Exercise
from fitness.validation import ensure_count, ensure_positive


class FlexibilityExercise(Exercise):
    """Растяжка с удержанием позы."""

    CATEGORY = "растяжка"

    def __init__(self, name, primary_muscle, difficulty, hold_seconds, bilateral=True, met_value=2.5):
        super().__init__(name, primary_muscle, difficulty, met_value)
        self._hold_seconds = ensure_positive(hold_seconds, "удержание")
        self._bilateral = bool(bilateral)

    @property
    def hold_seconds(self):
        return self._hold_seconds

    @property
    def bilateral(self):
        return self._bilateral

    def total_hold_time(self, rounds):
        ensure_count(rounds, "подходы", minimum=1)
        sides = 2 if self._bilateral else 1
        return self._hold_seconds * rounds * sides

    def extend_hold(self, extra_seconds):
        self._hold_seconds += ensure_positive(extra_seconds, "добавка к удержанию")
