from datetime import date

from culinary.validation import is_number
from .stock_item import StockItem
from .warehouse import Warehouse


class Inventory:
    """Акт инвентаризации: фактические остатки против учётных."""

    def __init__(self, warehouse, counted_by, counted_items=None, inventory_date=None):
        if not isinstance(warehouse, Warehouse):
            raise TypeError("Ожидается объект Warehouse")
        self.__warehouse = warehouse
        self.__counted_by = counted_by
        self.__inventory_date = inventory_date or date.today()
        self.__counted_items = {}
        for stock_item, actual in (counted_items or {}).items():
            self.record_count(stock_item, actual)

    @property
    def warehouse(self):
        return self.__warehouse

    @property
    def counted_by(self):
        return self.__counted_by

    @property
    def counted_items(self):
        return dict(self.__counted_items)

    @property
    def inventory_date(self):
        return self.__inventory_date

    def record_count(self, stock_item, actual_quantity):
        if not isinstance(stock_item, StockItem):
            raise TypeError("Ожидается объект StockItem")
        if stock_item not in self.__warehouse.stock_items:
            raise ValueError("Позиция не принадлежит инвентаризируемому складу")
        if not is_number(actual_quantity) or actual_quantity < 0:
            raise ValueError("Фактический остаток не может быть отрицательным")
        self.__counted_items[stock_item] = actual_quantity

    def find_discrepancies(self):
        return {
            item: actual - item.quantity_kg
            for item, actual in self.__counted_items.items()
            if actual != item.quantity_kg
        }

    def find_uncounted(self):
        return [item for item in self.__warehouse.stock_items if item not in self.__counted_items]

    def is_balanced(self):
        return not self.find_discrepancies() and not self.find_uncounted()
