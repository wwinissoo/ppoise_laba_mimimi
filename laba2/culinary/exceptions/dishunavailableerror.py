from .culinaryerror import CulinaryError

class DishUnavailableError(CulinaryError):
    """Блюдо недоступно."""

    def __init__(self, message="Блюдо недоступно"):
        super().__init__(message)
