"""Класс салата."""

from .dish import Dish
from .sauce import Sauce


class Salad(Dish):
    """Блюдо, которое обычно подают холодным."""

    CHILLED_LIMIT = 15
    DEFAULT_TEMPERATURE = 12

    def __init__(self, name, recipe, portions, serving_temperature=DEFAULT_TEMPERATURE, dressing=None):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__dressing = None
        if dressing is not None:
            self.add_dressing(dressing)

    @property
    def dressing(self):
        return self.__dressing

    def add_dressing(self, dressing):
        if not isinstance(dressing, Sauce):
            raise TypeError("Заправка должна быть объектом Sauce")
        self.__dressing = dressing

    def is_served_chilled(self):
        return self.serving_temperature <= self.CHILLED_LIMIT
