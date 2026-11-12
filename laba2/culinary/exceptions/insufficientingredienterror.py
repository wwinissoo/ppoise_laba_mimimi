from .culinaryerror import CulinaryError

class InsufficientIngredientError(CulinaryError):
    """Недостаточно ингредиента."""

    def __init__(self, message="Недостаточно ингредиента"):
        super().__init__(message)
