from datetime import date

from fitness.exceptions import InvalidValueError
from fitness.nutrition.macro_targets import MacroTargets
from fitness.nutrition.meal import Meal
from fitness.nutrition.supplement import Supplement
from fitness.users.user import User
from fitness.validation import ensure_count, ensure_instance, ensure_positive


class NutritionDiary:
    """Дневник питания пользователя за один день."""

    WATER_ML_PER_KG = 30

    def __init__(self, user, day, calorie_target):
        self._user = ensure_instance(user, User, "пользователь")
        self._day = ensure_instance(day, date, "день")
        self._calorie_target = ensure_positive(calorie_target, "цель по калориям")
        self._meals = []
        self._water_ml = 0
        self._supplements = []

    @property
    def user(self):
        return self._user

    @property
    def day(self):
        return self._day

    @property
    def calorie_target(self):
        return self._calorie_target

    @property
    def meals(self):
        return tuple(self._meals)

    @property
    def water_ml(self):
        return self._water_ml

    @property
    def supplements(self):
        return tuple(self._supplements)

    def take_supplement(self, supplement, doses=1):
        ensure_instance(supplement, Supplement, "добавка")
        supplement.take(doses)
        if supplement not in self._supplements:
            self._supplements.append(supplement)
        return supplement.remaining_mg()

    def add_meal(self, meal):
        ensure_instance(meal, Meal, "приём пищи")
        if meal.eaten_at.date() != self._day:
            raise InvalidValueError("Приём пищи относится к другому дню")
        self._meals.append(meal)
        self._meals.sort(key=lambda item: item.eaten_at)
        return meal

    def drink_water(self, milliliters):
        self._water_ml += ensure_count(milliliters, "вода, мл", minimum=1)
        return self._water_ml

    def total_calories(self):
        return round(sum(meal.total_calories() for meal in self._meals), 1)

    def remaining_calories(self):
        return round(self._calorie_target - self.total_calories(), 1)

    def is_over_target(self):
        return self.remaining_calories() < 0

    def total_macros(self):
        totals = dict.fromkeys(Meal.MACROS, 0.0)
        for meal in self._meals:
            for macro, grams in meal.macros().items():
                totals[macro] = round(totals[macro] + grams, 1)
        return totals

    def water_goal_ml(self):
        latest = self._user.latest_measurement()
        if latest is None:
            raise InvalidValueError("Для нормы воды нужен хотя бы один замер веса")
        return round(latest.weight_kg * self.WATER_ML_PER_KG)

    def macro_report(self, targets):
        ensure_instance(targets, MacroTargets, "нормы БЖУ")
        return targets.deviation(self.total_macros())
