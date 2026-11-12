"""Операции инвентаризации склада."""
class InventoryManager:
    def __init__(self,warehouse): self.__warehouse=warehouse
    @property
    def warehouse(self): return self.__warehouse
    def calculate_stock_value(self):
        return sum(item.ingredient.price_per_kg*item.quantity_kg for item in self.warehouse.stock_items)
    def find_reorder_candidates(self): return [item for item in self.warehouse.stock_items if item.quantity_kg < item.minimum_kg]
    def create_inventory_report(self):
        return {item.ingredient.name:item.quantity_kg for item in self.warehouse.stock_items}
