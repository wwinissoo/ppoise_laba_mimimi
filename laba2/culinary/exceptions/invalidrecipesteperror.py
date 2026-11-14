from .culinaryerror import CulinaryError
from .invalid_recipe_exception import InvalidRecipeException


class InvalidRecipeStepError(CulinaryError, InvalidRecipeException):
    """Некорректный шаг рецепта."""

    def __init__(self, message="Некорректный шаг рецепта"):
        super().__init__(message)
