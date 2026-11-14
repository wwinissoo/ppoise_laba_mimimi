from culinary.units import GRAMS_PER_KILOGRAM
from culinary.exceptions import (
    InsufficientIngredientError,
    WarehouseCapacityError,
)
from culinary.validation import is_number, require_text
from .stock_item import StockItem


class Warehouse:
    """Склад, хранящий остатки в килограммах в оперативной памяти."""

    DEFAULT_CAPACITY_KG = 1000

    def __init__(self, name, location, stock_items=None, capacity_kg=DEFAULT_CAPACITY_KG):
        if not is_number(capacity_kg) or capacity_kg < 0:
            raise WarehouseCapacityError("Вместимость склада не может быть отрицательной")
        self.__name = require_text(name, "Название склада не может быть пустым")
        self.__location = str(location or "").strip()
        self.__capacity_kg = capacity_kg
        self.__stock_items = []
        for item in stock_items or []:
            self.add_stock_item(item)

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self.__location

    @property
    def stock_items(self):
        return tuple(self.__stock_items)

    @property
    def capacity_kg(self):
        return self.__capacity_kg

    def calculate_total_weight(self):
        return sum(item.quantity_kg for item in self.__stock_items)

    def calculate_free_capacity(self):
        return self.__capacity_kg - self.calculate_total_weight()

    def has_free_capacity(self, incoming_kg):
        if not is_number(incoming_kg) or incoming_kg < 0:
            raise ValueError("Объем поставки должен быть неотрицательным числом")
        return incoming_kg <= self.calculate_free_capacity()

    def add_stock_item(self, stock_item):
        """Добавляет складскую позицию с контролем общей вместимости."""
        if not isinstance(stock_item, StockItem):
            raise TypeError("Ожидается объект StockItem")
        if self.get_stock_item(stock_item.ingredient) is not None:
            raise ValueError("Ингредиент уже зарегистрирован на складе")
        if not self.has_free_capacity(stock_item.quantity_kg):
            raise WarehouseCapacityError("Недостаточно места на складе")
        self.__stock_items.append(stock_item)
        return True

    def remove_stock_item(self, ingredient):
        item = self.get_stock_item(ingredient)
        if item is None:
            return False
        if item.quantity_kg != 0:
            raise ValueError("Можно удалить только пустую складскую позицию")
        self.__stock_items.remove(item)
        return True

    def get_stock_item(self, ingredient):
        name = ingredient if isinstance(ingredient, str) else ingredient.name
        key = name.strip().casefold()
        return next(
            (item for item in self.__stock_items if item.ingredient.name.casefold() == key),
            None,
        )

    def get_available_quantity(self, ingredient):
        item = self.get_stock_item(ingredient)
        return 0 if item is None else item.quantity_kg

    def find_expired(self):
        return [item for item in self.__stock_items if not item.ingredient.check_expiration()]

    def write_off_expired(self):
        """Списывает весь остаток просроченных позиций; возвращает списанный вес, кг."""
        written_off = 0
        for item in self.find_expired():
            if item.quantity_kg > 0:
                written_off += item.quantity_kg
                item.withdraw(item.quantity_kg)
            if item.ingredient.weight > 0:
                item.ingredient.consume(item.ingredient.weight)
        return written_off

    def deduct_ingredient(self, ingredient, amount_kg):
        if not is_number(amount_kg) or amount_kg <= 0:
            raise ValueError("Списываемое количество должно быть положительным")
        item = self.get_stock_item(ingredient)
        if item is None or item.quantity_kg < amount_kg:
            raise InsufficientIngredientError(f"Недостаточно «{ingredient.name}» на складе")
        if item.ingredient is not ingredient:
            raise InsufficientIngredientError(f"Складская партия «{ingredient.name}» не соответствует рецепту")
        ingredient.require_fresh()
        amount_grams = amount_kg * GRAMS_PER_KILOGRAM
        if ingredient.weight < amount_grams:
            raise InsufficientIngredientError(f"Недостаточно «{ingredient.name}» в партии ингредиента")
        item.withdraw(amount_kg)
        ingredient.consume(amount_grams)
