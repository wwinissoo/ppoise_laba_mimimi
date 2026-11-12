from culinary.exceptions import DishUnavailableError
class MenuItem:
    """Объект предметной области: MenuItem."""

    def __init__(self, dish, price, available, category):
        self.__dish = dish
        self.__price = price
        self.__available = available
        self.__category = category

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
        if not 0 <= percent <= 100: raise ValueError('Скидка должна быть от 0 до 100')
        self.__price *= (100 - percent) / 100


    def require_available(self):
        """Вызывает доменное исключение, если позицию нельзя заказать."""
        if not self.available:
            raise DishUnavailableError(f"Блюдо «{self.dish.name}» временно недоступно")
        return True
