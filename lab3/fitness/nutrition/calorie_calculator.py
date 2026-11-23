from datetime import date

from fitness.exceptions import InvalidValueError
from fitness.users.body_measurement import BodyMeasurement
from fitness.users.user import User
from fitness.validation import ensure_choice, ensure_instance


class CalorieCalculator:
    """Формула Миффлина — Сан Жеора с коэффициентом активности."""

    ACTIVITY_FACTORS = {"минимальная": 1.2, "низкая": 1.375, "средняя": 1.55, "высокая": 1.725, "экстремальная": 1.9}
    GOAL_ADJUSTMENTS = {"похудение": -500, "поддержание": 0, "набор массы": 300}
    MIN_SAFE_CALORIES = {User.MALE: 1500, User.FEMALE: 1200}
    GENDER_CONSTANTS = {User.MALE: 5, User.FEMALE: -161}

    def __init__(self, activity_level="средняя"):
        self._activity_level = ensure_choice(activity_level, set(self.ACTIVITY_FACTORS), "уровень активности")

    @property
    def activity_level(self):
        return self._activity_level

    def change_activity_level(self, level):
        self._activity_level = ensure_choice(level, set(self.ACTIVITY_FACTORS), "уровень активности")

    def _measurement(self, user, measurement):
        ensure_instance(user, User, "пользователь")
        measurement = measurement or user.latest_measurement()
        if measurement is None:
            raise InvalidValueError("Для расчёта нужен замер веса и роста")
        return ensure_instance(measurement, BodyMeasurement, "замер")

    def basal_metabolic_rate(self, user, today=None, measurement=None):
        measurement = self._measurement(user, measurement)
        age = user.age(today or date.today())
        bmr = 10 * measurement.weight_kg + 6.25 * measurement.height_cm - 5 * age
        return round(bmr + self.GENDER_CONSTANTS[user.gender])

    def daily_energy_expenditure(self, user, today=None, measurement=None):
        bmr = self.basal_metabolic_rate(user, today, measurement)
        return round(bmr * self.ACTIVITY_FACTORS[self._activity_level])

    def calorie_target(self, user, goal, today=None, measurement=None):
        ensure_choice(goal, set(self.GOAL_ADJUSTMENTS), "цель питания")
        target = self.daily_energy_expenditure(user, today, measurement) + self.GOAL_ADJUSTMENTS[goal]
        return max(target, self.MIN_SAFE_CALORIES[user.gender])
