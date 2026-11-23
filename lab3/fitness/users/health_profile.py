from fitness.exceptions import InjuryRiskError, InvalidMeasurementError, InvalidValueError
from fitness.exercises.balance_exercise import BalanceExercise
from fitness.users.injury import Injury
from fitness.validation import ensure_instance, ensure_number, ensure_text


class HealthProfile:
    """Медицинские показатели и ограничения пользователя."""

    HYPERTENSION_SYSTOLIC = 140
    HYPERTENSION_DIASTOLIC = 90

    def __init__(self, resting_heart_rate, systolic_pressure=120, diastolic_pressure=80):
        self._resting_heart_rate = self._reading(resting_heart_rate, "пульс в покое", 25, 150)
        self._systolic_pressure = self._reading(systolic_pressure, "систолическое давление", 60, 260)
        self._diastolic_pressure = self._reading(diastolic_pressure, "диастолическое давление", 30, 160)
        self._injuries = []
        self._chronic_conditions = []

    @staticmethod
    def _reading(value, field_name, minimum, maximum):
        try:
            return ensure_number(value, field_name, minimum, maximum)
        except InvalidValueError as error:
            raise InvalidMeasurementError(str(error)) from None

    @property
    def resting_heart_rate(self):
        return self._resting_heart_rate

    @property
    def systolic_pressure(self):
        return self._systolic_pressure

    @property
    def diastolic_pressure(self):
        return self._diastolic_pressure

    @property
    def injuries(self):
        return tuple(self._injuries)

    @property
    def chronic_conditions(self):
        return tuple(self._chronic_conditions)

    def add_injury(self, injury):
        self._injuries.append(ensure_instance(injury, Injury, "травма"))

    def add_condition(self, condition):
        text = ensure_text(condition, "хроническое заболевание")
        if text.casefold() not in (item.casefold() for item in self._chronic_conditions):
            self._chronic_conditions.append(text)

    def active_injuries(self):
        return [injury for injury in self._injuries if injury.is_active()]

    def is_hypertensive(self):
        return (
            self._systolic_pressure >= self.HYPERTENSION_SYSTOLIC
            or self._diastolic_pressure >= self.HYPERTENSION_DIASTOLIC
        )

    def update_pressure(self, systolic, diastolic):
        if systolic <= diastolic:
            raise InvalidMeasurementError("Систолическое давление должно быть выше диастолического")
        self._systolic_pressure = self._reading(systolic, "систолическое давление", 60, 260)
        self._diastolic_pressure = self._reading(diastolic, "диастолическое давление", 30, 160)

    def max_heart_rate(self, age):
        """Формула Танаки: 208 − 0,7 × возраст."""
        return round(208 - 0.7 * age)

    def heart_rate_reserve(self, age):
        return self.max_heart_rate(age) - self._resting_heart_rate

    def check_exercise_allowed(self, exercise):
        for muscle in exercise.involved_muscles():
            for injury in self.active_injuries():
                if injury.affects(muscle):
                    raise InjuryRiskError(f"«{exercise.name}» нагружает травмированную группу «{muscle.name}»")
        return True

    def needs_spotter(self, exercise):
        ensure_instance(exercise, BalanceExercise, "упражнение на баланс")
        return exercise.requires_support() or self.is_hypertensive() or bool(self.active_injuries())
