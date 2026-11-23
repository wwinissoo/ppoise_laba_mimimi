from fitness.exceptions import InvalidValueError
from fitness.exercises.exercise import Exercise
from fitness.validation import ensure_positive


class CardioExercise(Exercise):
    """Кардионагрузка с оценкой ударной нагрузки на суставы."""

    CATEGORY = "кардио"
    LOW_IMPACT = "низкая"
    HIGH_IMPACT = "высокая"
    MINUTES_PER_HOUR = 60

    def __init__(
        self, name, primary_muscle, difficulty, met_value=8.0, equipment=(), secondary_muscles=(), impact=LOW_IMPACT
    ):
        super().__init__(name, primary_muscle, difficulty, met_value, equipment, secondary_muscles)
        if impact not in (self.LOW_IMPACT, self.HIGH_IMPACT):
            raise InvalidValueError("Ударная нагрузка должна быть «низкая» или «высокая»")
        self._impact = impact

    @property
    def impact(self):
        return self._impact

    def is_low_impact(self):
        return self._impact == self.LOW_IMPACT

    def pace_min_per_km(self, distance_km, minutes):
        ensure_positive(distance_km, "дистанция")
        return round(minutes / distance_km, 2)

    def speed_kmh(self, distance_km, minutes):
        ensure_positive(minutes, "минуты")
        return round(distance_km / minutes * self.MINUTES_PER_HOUR, 2)
