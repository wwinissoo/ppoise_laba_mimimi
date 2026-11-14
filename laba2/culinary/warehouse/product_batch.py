from datetime import date

from culinary.exceptions import InsufficientIngredientError
from culinary.ingredients.ingredient import Ingredient
from culinary.validation import is_number, require_text
from .supplier import Supplier


class ProductBatch:
    """Партия продукта от поставщика с датой поступления и остатком."""

    def __init__(self, ingredient, batch_code, received_date, quantity_kg, supplier):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Партия должна ссылаться на объект Ingredient")
        if not isinstance(supplier, Supplier):
            raise TypeError("Партия должна ссылаться на объект Supplier")
        if not isinstance(received_date, date):
            raise TypeError("Дата поступления должна быть объектом date")
        if not is_number(quantity_kg) or quantity_kg <= 0:
            raise ValueError("Количество в партии должно быть положительным")
        self.__ingredient = ingredient
        self.__batch_code = require_text(batch_code, "Код партии не может быть пустым")
        self.__received_date = received_date
        self.__quantity_kg = quantity_kg
        self.__supplier = supplier
        self.__used_kg = 0

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

    def is_expired(self, on_date=None):
        on_date = on_date or date.today()
        return (on_date - self.__received_date).days >= self.ingredient.expiration_days

    def use(self, amount_kg):
        if not is_number(amount_kg) or amount_kg <= 0:
            raise ValueError("Количество должно быть положительным")
        if amount_kg > self.remaining_quantity():
            raise InsufficientIngredientError(f"В партии {self.batch_code} недостаточно продукта")
        self.__used_kg += amount_kg

    def remaining_quantity(self):
        return self.__quantity_kg - self.__used_kg

    def assign_batch_code(self, prefix):
        prefix = require_text(prefix, "Префикс не может быть пустым")
        if not self.__batch_code.startswith(f"{prefix}-"):
            self.__batch_code = f"{prefix}-{self.__batch_code}"
        return self.__batch_code
