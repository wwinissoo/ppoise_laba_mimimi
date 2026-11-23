"""Напиток."""

from culinary.validation import require_number
from .dish import Dish


class Beverage(Dish):
    """Напиток с объёмом и типом подачи."""

    def __init__(self, name, recipe, portions, serving_temperature, volume_ml, is_carbonated=False):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__volume_ml = require_number(volume_ml, "Объём должен быть положительным", positive=True)
        self.__is_carbonated = bool(is_carbonated)

    @property
    def volume_ml(self):
        return self.__volume_ml

    @property
    def is_carbonated(self):
        return self.__is_carbonated

    def dilute(self, added_water_ml):
        require_number(added_water_ml, "Объём воды должен быть положительным", positive=True)
        self.__volume_ml += added_water_ml
        return self.__volume_ml

    def serving_volume(self):
        return self.volume_ml / self.portions
