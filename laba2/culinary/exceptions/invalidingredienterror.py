from .culinaryerror import CulinaryError

class InvalidIngredientError(CulinaryError):
    """Некорректные данные ингредиента."""

    def __init__(self, message="Некорректные данные ингредиента"):
        super().__init__(message)
