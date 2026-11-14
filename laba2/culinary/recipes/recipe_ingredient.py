from culinary.exceptions import InvalidIngredientError
from culinary.ingredients.ingredient import Ingredient
from culinary.validation import is_number


class RecipeIngredient:
    """Связь рецепта с ингредиентом, его количеством и единицей измерения."""

    GRAM_UNITS = frozenset({"г", "гр", "грамм", "грамма", "граммов", "g"})
    KILOGRAM_UNITS = frozenset({"кг", "килограмм", "килограмма", "килограммов", "kg"})

    def __init__(self, ingredient, amount, unit, is_optional):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Ингредиент рецепта должен быть объектом Ingredient")
        if not is_number(amount) or amount <= 0:
            raise InvalidIngredientError("Количество ингредиента должно быть положительным")
        if not isinstance(unit, str) or not unit.strip():
            raise InvalidIngredientError("Единица измерения не может быть пустой")
        self.to_grams(amount, unit)
        self.__ingredient = ingredient
        self.__amount = amount
        self.__unit = unit.strip()
        self.__is_optional = bool(is_optional)

    @property
    def ingredient(self):
        return self.__ingredient

    @property
    def amount(self):
        return self.__amount

    @property
    def unit(self):
        return self.__unit

    @property
    def is_optional(self):
        return self.__is_optional

    @classmethod
    def to_grams(cls, amount, unit):
        normalized = unit.strip().casefold()
        if normalized in cls.GRAM_UNITS:
            return amount
        if normalized in cls.KILOGRAM_UNITS:
            return amount * Ingredient.GRAMS_PER_KILOGRAM
        raise InvalidIngredientError(f"Неизвестная единица измерения «{unit}»; допустимы г и кг")

    @classmethod
    def to_kilograms(cls, amount, unit):
        return cls.to_grams(amount, unit) / Ingredient.GRAMS_PER_KILOGRAM

    def amount_in_grams(self, multiplier=1):
        return self.to_grams(self.amount * multiplier, self.unit)

    def amount_in_kilograms(self, multiplier=1):
        return self.to_kilograms(self.amount * multiplier, self.unit)

    def calculate_cost(self):
        return self.ingredient.calculate_cost(self.amount_in_grams())

    def calculate_calories(self):
        return self.ingredient.calculate_calories(self.amount_in_grams())

    def consume_from_stock(self):
        self.ingredient.require_fresh()
        self.ingredient.consume(self.amount_in_grams())

    def describe_amount(self):
        return f"{self.amount:g} {self.unit} {self.ingredient.name}"
