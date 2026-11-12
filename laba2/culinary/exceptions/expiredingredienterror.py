from .culinaryerror import CulinaryError

class ExpiredIngredientError(CulinaryError):
    """Срок годности ингредиента истёк."""

    def __init__(self, message="Срок годности ингредиента истёк"):
        super().__init__(message)
