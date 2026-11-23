from datetime import date, timedelta

from fitness.exceptions import InvalidValueError
from fitness.exercises.flexibility_exercise import FlexibilityExercise
from fitness.exercises.muscle_group import MuscleGroup
from fitness.validation import ensure_choice, ensure_instance


class Injury:
    """Травма, ограничивающая нагрузку на группу мышц."""

    MILD = "лёгкая"
    MODERATE = "средняя"
    SEVERE = "тяжёлая"
    RECOVERY_DAYS = {MILD: 7, MODERATE: 21, SEVERE: 60}

    def __init__(self, muscle_group, severity, occurred_on, description=""):
        self._muscle_group = ensure_instance(muscle_group, MuscleGroup, "группа мышц")
        self._severity = ensure_choice(severity, set(self.RECOVERY_DAYS), "тяжесть травмы")
        self._occurred_on = ensure_instance(occurred_on, date, "дата травмы")
        self._description = description.strip() if isinstance(description, str) else ""
        self._recovered_on = None

    @property
    def muscle_group(self):
        return self._muscle_group

    @property
    def severity(self):
        return self._severity

    @property
    def occurred_on(self):
        return self._occurred_on

    @property
    def description(self):
        return self._description

    @property
    def recovered_on(self):
        return self._recovered_on

    def is_active(self):
        return self._recovered_on is None

    def mark_recovered(self, recovered_on):
        ensure_instance(recovered_on, date, "дата восстановления")
        if recovered_on < self._occurred_on:
            raise InvalidValueError("Восстановление не может быть раньше травмы")
        self._recovered_on = recovered_on

    def affects(self, muscle_group):
        return self.is_active() and self._muscle_group == muscle_group

    def allows_stretching(self, exercise):
        ensure_instance(exercise, FlexibilityExercise, "растяжка")
        if not self.is_active() or not self.affects(exercise.primary_muscle):
            return True
        return self._severity == self.MILD

    def expected_recovery_date(self):
        return self._occurred_on + timedelta(days=self.RECOVERY_DAYS[self._severity])
