class NutritionFacts:
    """Объект предметной области: NutritionFacts."""

    def __init__(self, calories, protein, fat, carbohydrates, serving_grams):
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
        return self.protein * 4 + self.carbohydrates * 4 + self.fat * 9

    def scale_to_serving(self, grams):
        if grams <= 0 or self.serving_grams <= 0: raise ValueError('Вес порции должен быть положительным')
        factor = grams / self.serving_grams
        return {'calories': self.calories * factor, 'protein': self.protein * factor, 'fat': self.fat * factor, 'carbohydrates': self.carbohydrates * factor}

    def is_high_protein(self, minimum=20):
        return self.protein >= minimum

