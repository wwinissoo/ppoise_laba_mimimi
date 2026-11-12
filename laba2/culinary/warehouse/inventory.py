class Inventory:
    """Объект предметной области: Inventory."""

    def __init__(self, warehouse, counted_by, counted_items, inventory_date):
        self.__warehouse = warehouse
        self.__counted_by = counted_by
        self.__counted_items = counted_items
        self.__inventory_date = inventory_date

    @property
    def warehouse(self):
        return self.__warehouse

    @property
    def counted_by(self):
        return self.__counted_by

    @property
    def counted_items(self):
        return self.__counted_items

    @property
    def inventory_date(self):
        return self.__inventory_date

    def record_count(self, stock_item, actual_quantity):
        self.counted_items[stock_item] = actual_quantity

    def find_discrepancies(self):
        return {item: actual - item.quantity_kg for item, actual in self.counted_items.items() if actual != item.quantity_kg}

    def is_balanced(self):
        return len(self.find_discrepancies()) == 0

