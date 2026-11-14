from culinary.units import PERCENT
from culinary.exceptions import PortionException
from culinary.validation import require_number


class NutritionFacts:
    """Пищевая ценность (КБЖУ) на заданную массу порции."""

    HIGH_PROTEIN_PER_100G = 20
    KCAL_PER_GRAM = {"protein": 4, "fat": 9, "carbohydrates": 4}

    def __init__(self, calories, protein, fat, carbohydrates, serving_grams):
        for value in (calories, protein, fat, carbohydrates):
            require_number(value, "Показатели пищевой ценности не могут быть отрицательными", minimum=0)
        require_number(serving_grams, "Вес порции должен быть положительным", PortionException, positive=True)
        if protein + fat + carbohydrates > serving_grams:
            raise ValueError("Сумма БЖУ не может превышать массу порции")
        self.__calories = calories
        self.__protein = protein
        self.__fat = fat
        self.__carbohydrates = carbohydrates
        self.__serving_grams = serving_grams

    @property
    def calories(self):
        return self.__calories

    @property
    def protein(self):
        return self.__protein

    @property
    def fat(self):
        return self.__fat

    @property
    def carbohydrates(self):
        return self.__carbohydrates

    @property
    def serving_grams(self):
        return self.__serving_grams

    def calculate_energy_from_macros(self):
        return (
            self.protein * self.KCAL_PER_GRAM["protein"]
            + self.carbohydrates * self.KCAL_PER_GRAM["carbohydrates"]
            + self.fat * self.KCAL_PER_GRAM["fat"]
        )

    def scale_to_serving(self, grams):
        require_number(grams, "Вес порции должен быть положительным", PortionException, positive=True)
        factor = grams / self.serving_grams
        return {
            "calories": self.calories * factor,
            "protein": self.protein * factor,
            "fat": self.fat * factor,
            "carbohydrates": self.carbohydrates * factor,
        }

    def is_high_protein(self, minimum=HIGH_PROTEIN_PER_100G):
        """Не менее minimum граммов белка на 100 г продукта."""
        return self.protein / self.serving_grams * PERCENT >= minimum
