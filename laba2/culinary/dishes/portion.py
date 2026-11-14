from culinary.exceptions import PortionException
from culinary.validation import require_number, require_positive_int
from .dish import Dish


class Portion:
    """Конкретная порция блюда, поданная к столику."""

    def __init__(self, dish, weight, price, table_number):
        if not isinstance(dish, Dish):
            raise TypeError("Порция должна ссылаться на объект Dish")
        require_number(weight, "Вес порции должен быть положительным", PortionException, positive=True)
        require_number(price, "Цена порции не может быть отрицательной", PortionException, 0)
        require_positive_int(table_number, "Номер столика должен быть положительным целым числом", PortionException)
        self.__dish = dish
        self.__weight = weight
        self.__price = price
        self.__table_number = table_number

    @property
    def dish(self):
        return self.__dish

    @property
    def weight(self):
        return self.__weight

    @property
    def price(self):
        return self.__price

    @property
    def table_number(self):
        return self.__table_number

    def calculate_price_per_gram(self):
        return self.price / self.weight

    def is_for_table(self, number):
        return self.table_number == number

    def increase_weight(self, grams):
        require_number(grams, "Добавка должна быть положительной", PortionException, positive=True)
        self.__weight += grams
