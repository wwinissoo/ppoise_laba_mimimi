from .culinaryerror import CulinaryError
from .insufficient_stock_exception import InsufficientStockException


class InsufficientIngredientError(CulinaryError, InsufficientStockException):
    """Недостаточно ингредиента."""

    def __init__(self, message="Недостаточно ингредиента"):
        super().__init__(message)
