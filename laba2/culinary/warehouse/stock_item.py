from culinary.exceptions import InsufficientIngredientError
from culinary.ingredients.ingredient import Ingredient
from culinary.validation import is_number, require_text


class StockItem:
    """Остаток одной ингредиентной партии в килограммах."""

    def __init__(self, ingredient, quantity_kg, minimum_kg=0, location_code="A-1"):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Складская позиция должна ссылаться на объект Ingredient")
        if not is_number(quantity_kg) or quantity_kg < 0:
            raise ValueError("Остаток должен быть неотрицательным числом")
        if not is_number(minimum_kg) or minimum_kg < 0:
            raise ValueError("Минимальный остаток должен быть неотрицательным числом")
        self.__ingredient = ingredient
        self.__quantity_kg = quantity_kg
        self.__minimum_kg = minimum_kg
        self.__location_code = require_text(location_code, "Код места хранения не может быть пустым")

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

    def calculate_shortage(self):
        return max(0, self.minimum_kg - self.quantity_kg)

    def withdraw(self, amount_kg):
        if not is_number(amount_kg) or amount_kg <= 0:
            raise ValueError("Списываемое количество должно быть положительным")
        if amount_kg > self.quantity_kg:
            raise InsufficientIngredientError(f"Недостаточный запас «{self.ingredient.name}»")
        self.__quantity_kg -= amount_kg

    def receive(self, amount_kg):
        if not is_number(amount_kg) or amount_kg <= 0:
            raise ValueError("Количество должно быть положительным")
        self.__quantity_kg += amount_kg

    def relocate(self, location_code):
        self.__location_code = require_text(location_code, "Код места хранения не может быть пустым")
