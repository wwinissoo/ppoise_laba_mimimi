"""Класс салата."""
from .dish import Dish
class Salad(Dish):
    """Блюдо, которое обычно подают холодным."""
    def __init__(self, name, recipe, portions, serving_temperature=12, dressing=None):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__dressing=dressing
    @property
    def dressing(self): return self.__dressing
    def add_dressing(self, dressing):
        if dressing is None: raise ValueError("Заправка не задана")
        self.__dressing=dressing
    def is_served_chilled(self): return self.serving_temperature <= 15
