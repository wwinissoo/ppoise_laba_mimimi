"""Складской запас."""

from .stock_item import StockItem


class Stock:
    """Индекс складских позиций по названию ингредиента."""

    def __init__(self):
        self.__items = {}

    @property
    def items(self):
        return tuple(self.__items.values())

    def add_item(self, stock_item):
        if not isinstance(stock_item, StockItem):
            raise TypeError("Ожидается объект StockItem")
        key = stock_item.ingredient.name.casefold()
        if key in self.__items:
            raise ValueError("Позиция с таким ингредиентом уже есть")
        self.__items[key] = stock_item

    def get_item(self, ingredient_name):
        return self.__items.get(ingredient_name.strip().casefold())

    def total_quantity(self):
        return sum(item.quantity_kg for item in self.__items.values())

    def below_minimum(self):
        return [item for item in self.__items.values() if item.needs_restock()]
