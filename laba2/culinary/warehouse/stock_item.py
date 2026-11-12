class StockItem:
    """Объект предметной области: StockItem."""

    def __init__(self, ingredient, quantity_kg, minimum_kg, location_code):
        self.__ingredient = ingredient
        self.__quantity_kg = quantity_kg
        self.__minimum_kg = minimum_kg
        self.__location_code = location_code

    @property
    def ingredient(self):
        return self.__ingredient

    @property
    def quantity_kg(self):
        return self.__quantity_kg

    @property
    def minimum_kg(self):
        return self.__minimum_kg

    @property
    def location_code(self):
        return self.__location_code

    def needs_restock(self):
        return self.quantity_kg < self.minimum_kg

    def withdraw(self, amount_kg):
        if amount_kg <= 0 or amount_kg > self.quantity_kg: raise ValueError('Недостаточный запас')
        self.__quantity_kg -= amount_kg

    def receive(self, amount_kg):
        if amount_kg <= 0: raise ValueError('Количество должно быть положительным')
        self.__quantity_kg += amount_kg

