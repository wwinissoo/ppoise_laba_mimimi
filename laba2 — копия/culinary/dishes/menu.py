from datetime import date

from culinary.exceptions import DishUnavailableError
from culinary.validation import require_text
from .dish import Dish


class Menu:
    """Меню на период действия: набор блюд без повторов."""

    def __init__(self, title, dishes=None, valid_from=None, valid_to=None):
        self.__title = require_text(title, "Название меню не может быть пустым")
        if valid_from is not None and valid_to is not None and valid_from > valid_to:
            raise ValueError("Дата начала меню не может быть позже даты окончания")
        self.__valid_from = valid_from
        self.__valid_to = valid_to
        self.__dishes = []
        for dish in dishes or []:
            self.add_dish(dish)

    @property
    def title(self):
        return self.__title

    @property
    def dishes(self):
        return tuple(self.__dishes)

    @property
    def valid_from(self):
        return self.__valid_from

    @property
    def valid_to(self):
        return self.__valid_to

    def add_dish(self, dish):
        if not isinstance(dish, Dish):
            raise TypeError("В меню можно добавить только Dish")
        if self.find_dish(dish.name) is not None:
            raise DishUnavailableError(f"Блюдо «{dish.name}» уже есть в меню")
        self.__dishes.append(dish)

    def remove_dish(self, dish):
        if dish in self.__dishes:
            self.__dishes.remove(dish)
            return True
        return False

    def find_dish(self, name):
        key = name.strip().casefold()
        return next((dish for dish in self.__dishes if dish.name.casefold() == key), None)

    def find_dishes_under_price(self, maximum):
        """Блюда, себестоимость порции которых не превышает maximum."""
        return [dish for dish in self.__dishes if dish.calculate_cost_per_portion() <= maximum]

    def is_active(self, on_date=None):
        on_date = on_date or date.today()
        return (self.__valid_from is None or self.__valid_from <= on_date) and (
            self.__valid_to is None or on_date <= self.__valid_to
        )
