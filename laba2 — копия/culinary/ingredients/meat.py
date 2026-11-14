from culinary.units import PERCENT
from culinary.ingredients.ingredient import Ingredient
from culinary.exceptions import InvalidIngredientError


class Meat(Ingredient):
    """Класс Meat предметной области «Кулинария»."""

    DEFAULT_FAT_PERCENTAGE = 10
    PERCENT_MIN = 0
    PERCENT_MAX = 100

    def __init__(
        self,
        name,
        weight,
        price_per_kg,
        calories,
        expiration_days,
        storage_temperature,
        fat_percentage=DEFAULT_FAT_PERCENTAGE,
        meat_type="говядина",
        is_frozen=False,
    ):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not self.PERCENT_MIN <= fat_percentage <= self.PERCENT_MAX:
            raise InvalidIngredientError("Жирность должна быть от 0 до 100")
        self.__fat_percentage = fat_percentage
        self.__meat_type = meat_type
        self.__is_frozen = bool(is_frozen)
        self.__is_marinated = False

    @property
    def fat_percentage(self):
        return self.__fat_percentage

    @property
    def meat_type(self):
        return self.__meat_type

    @property
    def is_frozen(self):
        return self.__is_frozen

    @property
    def is_marinated(self):
        return self.__is_marinated

    def defrost(self):
        self.__is_frozen = False
        return self.__is_frozen

    def marinate(self, marinade):
        if not isinstance(marinade, str) or not marinade.strip():
            raise InvalidIngredientError("Нужно указать маринад")
        self.__is_marinated = True
        return marinade.strip()

    def calculate_fat_weight(self):
        return self.weight * self.__fat_percentage / PERCENT

    def check_fat_content(self, maximum):
        return self.__fat_percentage <= maximum
