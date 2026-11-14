from .culinaryerror import CulinaryError
from .expired_product_exception import ExpiredProductException


class ExpiredIngredientError(CulinaryError, ExpiredProductException):
    """Срок годности ингредиента истёк."""

    def __init__(self, message="Срок годности ингредиента истёк"):
        super().__init__(message)
