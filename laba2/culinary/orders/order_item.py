class OrderItem:
    """Объект предметной области: OrderItem."""

    def __init__(self, dish, quantity, unit_price, note):
        self.__dish = dish
        self.__quantity = quantity
        self.__unit_price = unit_price
        self.__note = note

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
        if amount <= 0: raise ValueError('Количество должно быть положительным')
        self.__quantity += amount

    def add_note(self, note):
        self.__note = note

