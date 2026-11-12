from culinary.ingredients.ingredient import Ingredient
from culinary.exceptions import InvalidIngredientError

class Spice(Ingredient):
    """Класс Spice предметной области «Кулинария»."""
    INTENSITY_MIN = 0
    INTENSITY_MAX = 10
    """Модель ингредиента типа Spice."""
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 intensity=5, flavor="пряный", is_ground=False):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not self.INTENSITY_MIN <= intensity <= self.INTENSITY_MAX:
            raise InvalidIngredientError("Острота должна быть от 0 до 10")
        self.__intensity = intensity
        self.__flavor = flavor
        self.__is_ground = bool(is_ground)
        self.__is_mixed = False

    @property
    def intensity(self): return self.__intensity
    @property
    def flavor(self): return self.__flavor
    @property
    def is_ground(self): return self.__is_ground
    @property
    def is_mixed(self): return self.__is_mixed

    def grind(self):
        self.__is_ground = True
        return self.__is_ground

    def mix_with(self, other_spice):
        if not isinstance(other_spice, Spice):
            raise TypeError("Можно смешивать только специи")
        self.__is_mixed = True
        return (self.__intensity + other_spice.intensity) / 2

    def adjust_intensity(self, value):
        if not self.INTENSITY_MIN <= value <= self.INTENSITY_MAX:
            raise InvalidIngredientError("Острота должна быть от 0 до 10")
        self.__intensity = value

    def describe_flavor(self):
        return f"{self.flavor}, интенсивность {self.__intensity}/10"
