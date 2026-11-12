from culinary.exceptions import InvalidIngredientError, ExpiredIngredientError

class RecipeIngredient:
    """Связь рецепта с ингредиентом, его количеством и единицей измерения."""

    def __init__(self, ingredient, amount, unit, is_optional):
        if amount <= 0:
            raise InvalidIngredientError("Количество ингредиента должно быть положительным")
        if not isinstance(unit, str) or not unit.strip():
            raise InvalidIngredientError("Единица измерения не может быть пустой")
        self.__ingredient = ingredient
        self.__amount = amount
        self.__unit = unit.strip()
        self.__is_optional = bool(is_optional)

    @property
    def ingredient(self): return self.__ingredient
    @property
    def amount(self): return self.__amount
    @property
    def unit(self): return self.__unit
    @property
    def is_optional(self): return self.__is_optional

    def calculate_cost(self):
        self.ingredient.require_fresh()
        return self.ingredient.calculate_cost(self.amount)

    def consume_from_stock(self):
        self.ingredient.require_fresh()
        self.ingredient.consume(self.amount)

    def describe_amount(self):
        return f"{self.amount:g} {self.unit} {self.ingredient.name}"
