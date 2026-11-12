"""Класс выпечки."""
from .dish import Dish
class Pastry(Dish):
    """Выпечка с температурой выпекания и временем в духовке."""
    def __init__(self, name, recipe, portions, serving_temperature, baking_temperature, baking_minutes):
        super().__init__(name, recipe, portions, serving_temperature)
        if baking_temperature < 0 or baking_minutes <= 0: raise ValueError("Некорректные параметры выпечки")
        self.__baking_temperature=baking_temperature
        self.__baking_minutes=baking_minutes
    @property
    def baking_temperature(self): return self.__baking_temperature
    @property
    def baking_minutes(self): return self.__baking_minutes
    def estimate_baking_end(self, start_minute): return start_minute + self.baking_minutes
    def is_baking_temperature_safe(self): return 0 < self.baking_temperature <= 300
