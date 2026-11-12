class ProductBatch:
    """Объект предметной области: ProductBatch."""

    def __init__(self, ingredient, batch_code, received_date, quantity_kg, supplier):
        self.__ingredient = ingredient
        self.__batch_code = batch_code
        self.__received_date = received_date
        self.__quantity_kg = quantity_kg
        self.__supplier = supplier

    @property
    def ingredient(self):
        return self.__ingredient

    @property
    def batch_code(self):
        return self.__batch_code

    @property
    def received_date(self):
        return self.__received_date

    @property
    def quantity_kg(self):
        return self.__quantity_kg

    @property
    def supplier(self):
        return self.__supplier

    def is_expired(self, days_since_receipt):
        return days_since_receipt >= self.ingredient.expiration_days

    def remaining_quantity(self):
        return self.quantity_kg

    def assign_batch_code(self, prefix):
        self.__batch_code = f'{prefix}-{self.batch_code}'

