from culinary.exceptions import WarehouseCapacityError
class Warehouse:
    """Объект предметной области: Warehouse."""

    def __init__(self, name, location, stock_items, capacity_kg):
        self.__name = name
        self.__location = location
        self.__stock_items = stock_items
        self.__capacity_kg = capacity_kg

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self.__location

    @property
    def stock_items(self):
        return self.__stock_items

    @property
    def capacity_kg(self):
        return self.__capacity_kg

    def calculate_total_weight(self):
        return sum(item.quantity_kg for item in self.stock_items)

    def has_free_capacity(self, incoming_kg):
        return self.calculate_total_weight() + incoming_kg <= self.capacity_kg


    def add_stock_item(self, stock_item):
        """Добавляет складскую позицию с контролем общей вместимости."""
        current = sum(item.quantity_kg for item in self.__stock_items)
        if current + stock_item.quantity_kg > self.__capacity_kg:
            raise WarehouseCapacityError("Недостаточно места на складе")
        self.__stock_items.append(stock_item)
        return True
