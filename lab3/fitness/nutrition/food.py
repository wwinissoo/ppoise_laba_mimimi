from fitness.exceptions import InvalidValueError
from fitness.nutrition.constants import BASE_GRAMS, PROTEIN_KCAL
from fitness.validation import ensure_number, ensure_positive, ensure_text


class Food:
    """Продукт с КБЖУ на 100 г."""

    HIGH_PROTEIN_SHARE = 0.3

    def __init__(self, name, calories_per_100g, protein_g, fat_g, carbs_g):
        self._name = ensure_text(name, "название продукта")
        self._calories_per_100g = ensure_number(calories_per_100g, "калорийность", 0, 900)
        self._protein_g = ensure_number(protein_g, "белки", 0, BASE_GRAMS)
        self._fat_g = ensure_number(fat_g, "жиры", 0, BASE_GRAMS)
        self._carbs_g = ensure_number(carbs_g, "углеводы", 0, BASE_GRAMS)
        if self._protein_g + self._fat_g + self._carbs_g > BASE_GRAMS:
            raise InvalidValueError("Сумма БЖУ не может превышать 100 г на 100 г продукта")

    @property
    def name(self):
        return self._name

    @property
    def calories_per_100g(self):
        return self._calories_per_100g

    @property
    def protein_g(self):
        return self._protein_g

    @property
    def fat_g(self):
        return self._fat_g

    @property
    def carbs_g(self):
        return self._carbs_g

    def nutrients_for(self, grams):
        ensure_number(grams, "граммы", minimum=0)
        factor = grams / BASE_GRAMS
        return {
            "калории": round(self._calories_per_100g * factor, 1),
            "белки": round(self._protein_g * factor, 1),
            "жиры": round(self._fat_g * factor, 1),
            "углеводы": round(self._carbs_g * factor, 1),
        }

    def is_high_protein(self):
        if self._calories_per_100g == 0:
            return False
        return self._protein_g * PROTEIN_KCAL / self._calories_per_100g >= self.HIGH_PROTEIN_SHARE

    def grams_for_calories(self, calories):
        ensure_positive(calories, "калории")
        if self._calories_per_100g == 0:
            raise InvalidValueError(f"«{self._name}» не содержит калорий")
        return round(calories / self._calories_per_100g * BASE_GRAMS, 1)
