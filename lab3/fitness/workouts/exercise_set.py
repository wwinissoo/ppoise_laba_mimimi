from fitness.exceptions import InvalidValueError
from fitness.validation import ensure_count, ensure_number


class ExerciseSet:
    """Один подход: повторения, вес, время и субъективная тяжесть (RPE)."""

    MIN_RPE = 1
    MAX_RPE = 10
    LIGHT_RPE_LIMIT = 6
    MODERATE_RPE_LIMIT = 8

    def __init__(self, reps, weight_kg=0, duration_seconds=0):
        self._reps = ensure_count(reps, "повторения")
        self._weight_kg = ensure_number(weight_kg, "вес", minimum=0)
        self._duration_seconds = ensure_number(duration_seconds, "длительность", minimum=0)
        if self._reps == 0 and self._duration_seconds == 0:
            raise InvalidValueError("Подход должен иметь повторения или длительность")
        self._rpe = None
        self._completed = False

    @property
    def reps(self):
        return self._reps

    @property
    def weight_kg(self):
        return self._weight_kg

    @property
    def duration_seconds(self):
        return self._duration_seconds

    @property
    def rpe(self):
        return self._rpe

    @property
    def completed(self):
        return self._completed

    def volume(self):
        return self._reps * self._weight_kg

    def complete(self, rpe):
        self._rpe = ensure_number(rpe, "RPE", self.MIN_RPE, self.MAX_RPE)
        self._completed = True

    def intensity_label(self):
        if self._rpe is None:
            return "не выполнен"
        if self._rpe <= self.LIGHT_RPE_LIMIT:
            return "лёгкий"
        if self._rpe <= self.MODERATE_RPE_LIMIT:
            return "средний"
        return "тяжёлый"
