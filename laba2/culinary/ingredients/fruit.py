from culinary.units import PERCENT
from culinary.ingredients.ingredient import Ingredient
from culinary.exceptions import InvalidIngredientError


class Fruit(Ingredient):
    """Класс Fruit предметной области «Кулинария»."""

    DEFAULT_SWEETNESS = 5
    SWEETNESS_MIN = 0
    SWEETNESS_MAX = 10

    def __init__(
        self,
        name,
        weight,
        price_per_kg,
        calories,
        expiration_days,
        storage_temperature,
        sweetness=DEFAULT_SWEETNESS,
        has_seeds=True,
        is_ripe=True,
    ):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not self.SWEETNESS_MIN <= sweetness <= self.SWEETNESS_MAX:
            raise InvalidIngredientError("Сладость должна быть от 0 до 10")
        self.__sweetness = sweetness
        self.__has_seeds = bool(has_seeds)
        self.__is_ripe = bool(is_ripe)
        self.__is_cut = False

    @property
    def sweetness(self):
        return self.__sweetness

    @property
    def has_seeds(self):
        return self.__has_seeds

    @property
    def is_ripe(self):
        return self.__is_ripe

    @property
    def is_cut(self):
        return self.__is_cut

    def ripen(self):
        self.__is_ripe = True
        return self.__is_ripe

    def cut(self):
        if not self.__is_ripe:
            raise InvalidIngredientError("Неспелый фрукт нельзя подготовить для подачи")
        self.__is_cut = True
        return self.weight

    def calculate_sweetness_score(self):
        return self.__sweetness * self.weight / PERCENT

    def remove_seeds(self):
        self.__has_seeds = False
        return True
