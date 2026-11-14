from .culinaryerror import CulinaryError
from .invalid_ingredient_exception import InvalidIngredientException


class InvalidIngredientError(CulinaryError, InvalidIngredientException):
    """Некорректные данные ингредиента."""

    def __init__(self, message="Некорректные данные ингредиента"):
        super().__init__(message)
