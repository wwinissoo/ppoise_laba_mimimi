"""Операции инвентаризации склада."""

from .warehouse import Warehouse


class InventoryManager:
    def __init__(self, warehouse):
        if not isinstance(warehouse, Warehouse):
            raise TypeError("Ожидается объект Warehouse")
        self.__warehouse = warehouse

    @property
    def warehouse(self):
        return self.__warehouse

    def calculate_stock_value(self):
        return sum(item.ingredient.price_per_kg * item.quantity_kg for item in self.warehouse.stock_items)

    def find_reorder_candidates(self):
        return [item for item in self.warehouse.stock_items if item.needs_restock()]

    def calculate_reorder_quantities(self):
        return {item.ingredient.name: item.calculate_shortage() for item in self.find_reorder_candidates()}

    def create_inventory_report(self):
        return {item.ingredient.name: item.quantity_kg for item in self.warehouse.stock_items}
