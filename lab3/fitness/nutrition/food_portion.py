from fitness.nutrition.food import Food
from fitness.validation import ensure_instance, ensure_positive


class FoodPortion:
    """Конкретная порция продукта в граммах."""

    def __init__(self, food, grams):
        self._food = ensure_instance(food, Food, "продукт")
        self._grams = ensure_positive(grams, "граммы")

    @property
    def food(self):
        return self._food

    @property
    def grams(self):
        return self._grams

    def nutrients(self):
        return self._food.nutrients_for(self._grams)

    def calories(self):
        return self.nutrients()["калории"]

    def scaled(self, factor):
        return FoodPortion(self._food, self._grams * ensure_positive(factor, "коэффициент"))
