"""Напиток."""
from .dish import Dish
class Beverage(Dish):
    """Напиток с объёмом и типом подачи."""
    def __init__(self, name, recipe, portions, serving_temperature, volume_ml, is_carbonated=False):
        super().__init__(name, recipe, portions, serving_temperature)
        if volume_ml <= 0: raise ValueError("Объём должен быть положительным")
        self.__volume_ml=volume_ml; self.__is_carbonated=bool(is_carbonated)
    @property
    def volume_ml(self): return self.__volume_ml
    @property
    def is_carbonated(self): return self.__is_carbonated
    def dilute(self, added_water_ml):
        if added_water_ml <= 0: raise ValueError("Объём воды должен быть положительным")
        self.__volume_ml += added_water_ml
        return self.__volume_ml
    def serving_volume(self): return self.volume_ml / self.portions
