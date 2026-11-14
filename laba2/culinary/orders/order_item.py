from culinary.dishes.dish import Dish
from culinary.validation import is_number, require_positive_int


class OrderItem:
    """Позиция заказа с проверкой количества и цены."""

    def __init__(self, dish, quantity, unit_price, note=""):
        if not isinstance(dish, Dish):
            raise TypeError("Позиция заказа должна ссылаться на объект Dish")
        self._validate_quantity(quantity)
        self._validate_price(unit_price)
        self.__dish = dish
        self.__quantity = quantity
        self.__unit_price = unit_price
        self.__note = str(note or "").strip()

    @staticmethod
    def _validate_quantity(quantity):
        require_positive_int(quantity, "Количество порций должно быть положительным целым числом", ValueError)

    @staticmethod
    def _validate_price(price):
        if not is_number(price) or price < 0:
            raise ValueError("Цена не может быть отрицательной")

    @property
    def dish(self):
        return self.__dish

    @property
    def quantity(self):
        return self.__quantity

    @property
    def unit_price(self):
        return self.__unit_price

    @property
    def note(self):
        return self.__note

    def calculate_total(self):
        return self.quantity * self.unit_price

    def increase_quantity(self, amount):
        self._validate_quantity(amount)
        self.__quantity += amount

    def update_quantity(self, quantity):
        self._validate_quantity(quantity)
        self.__quantity = quantity

    def update_unit_price(self, price):
        self._validate_price(price)
        self.__unit_price = price

    def add_note(self, note):
        note = str(note or "").strip()
        self.__note = f"{self.__note}; {note}" if self.__note and note else (note or self.__note)
