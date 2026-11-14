from culinary.units import PERCENT
from culinary.exceptions import DishUnavailableError
from culinary.validation import is_number, require_number, require_text
from .dish import Dish


class MenuItem:
    """Позиция меню: блюдо, его цена продажи, категория и доступность."""

    PRICE_PRECISION = 2

    def __init__(self, dish, price, available=True, category="основное"):
        if not isinstance(dish, Dish):
            raise TypeError("Позиция меню должна ссылаться на объект Dish")
        self.__dish = dish
        self.__price = require_number(price, "Цена не может быть отрицательной", minimum=0)
        self.__available = bool(available)
        self.__category = require_text(category, "Категория не может быть пустой")

    @property
    def dish(self):
        return self.__dish

    @property
    def price(self):
        return self.__price

    @property
    def available(self):
        return self.__available

    @property
    def category(self):
        return self.__category

    def mark_unavailable(self):
        self.__available = False

    def mark_available(self):
        self.__available = True

    def apply_discount(self, percent):
        if not is_number(percent) or not 0 <= percent <= PERCENT:
            raise ValueError("Скидка должна быть от 0 до 100")
        self.__price = round(self.__price * (PERCENT - percent) / PERCENT, self.PRICE_PRECISION)
        return self.__price

    def calculate_margin(self):
        """Наценка: цена продажи минус себестоимость порции."""
        return self.price - self.dish.calculate_cost_per_portion()

    def require_available(self):
        """Вызывает доменное исключение, если позицию нельзя заказать."""
        if not self.available:
            raise DishUnavailableError(f"Блюдо «{self.dish.name}» временно недоступно")
        return True
