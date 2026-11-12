"""Основное блюдо."""
from .dish import Dish
class MainCourse(Dish):
    """Основное блюдо с признаком наличия гарнира."""
    def __init__(self, name, recipe, portions, serving_temperature, side_dish=None):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__side_dish=side_dish
    @property
    def side_dish(self): return self.__side_dish
    def attach_side_dish(self, dish):
        if dish is None: raise ValueError("Гарнир не задан")
        self.__side_dish=dish
    def has_side_dish(self): return self.__side_dish is not None
