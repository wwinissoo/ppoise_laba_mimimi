from datetime import datetime

from fitness.exceptions import EntityNotFoundError
from fitness.nutrition.constants import CARB_KCAL, FAT_KCAL, PROTEIN_KCAL
from fitness.nutrition.food_portion import FoodPortion
from fitness.validation import ensure_choice, ensure_instance


class Meal:
    """Приём пищи из нескольких порций."""

    TYPES = {"завтрак", "обед", "ужин", "перекус"}
    MACROS = ("белки", "жиры", "углеводы")

    def __init__(self, meal_type, eaten_at):
        self._meal_type = ensure_choice(meal_type, self.TYPES, "тип приёма пищи")
        self._eaten_at = ensure_instance(eaten_at, datetime, "время приёма пищи")
        self._portions = []

    @property
    def meal_type(self):
        return self._meal_type

    @property
    def eaten_at(self):
        return self._eaten_at

    @property
    def portions(self):
        return tuple(self._portions)

    def add_portion(self, portion):
        self._portions.append(ensure_instance(portion, FoodPortion, "порция"))
        return portion

    def remove_food(self, food_name):
        for portion in self._portions:
            if portion.food.name.casefold() == food_name.casefold():
                self._portions.remove(portion)
                return portion
        raise EntityNotFoundError(f"В приёме пищи нет «{food_name}»")

    def total_calories(self):
        return round(sum(portion.calories() for portion in self._portions), 1)

    def macros(self):
        totals = dict.fromkeys(self.MACROS, 0.0)
        for portion in self._portions:
            nutrients = portion.nutrients()
            for macro in self.MACROS:
                totals[macro] = round(totals[macro] + nutrients[macro], 1)
        return totals

    def dominant_macro(self):
        macros = self.macros()
        energy = {"белки": macros["белки"] * PROTEIN_KCAL, "жиры": macros["жиры"] * FAT_KCAL}
        energy["углеводы"] = macros["углеводы"] * CARB_KCAL
        return max(energy, key=energy.get) if any(energy.values()) else None
