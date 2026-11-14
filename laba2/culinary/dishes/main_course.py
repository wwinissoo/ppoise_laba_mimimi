"""Основное блюдо."""

from .dish import Dish
from .garnish import Garnish


class MainCourse(Dish):
    """Основное блюдо с необязательным гарниром."""

    def __init__(self, name, recipe, portions, serving_temperature, side_dish=None):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__side_dish = None
        if side_dish is not None:
            self.attach_side_dish(side_dish)

    @property
    def side_dish(self):
        return self.__side_dish

    def attach_side_dish(self, garnish):
        if not isinstance(garnish, Garnish):
            raise TypeError("Гарнир должен быть объектом Garnish")
        self.__side_dish = garnish

    def has_side_dish(self):
        return self.__side_dish is not None
