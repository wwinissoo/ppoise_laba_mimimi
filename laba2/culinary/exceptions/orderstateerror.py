from .culinaryerror import CulinaryError

class OrderStateError(CulinaryError):
    """Недопустимое состояние заказа."""

    def __init__(self, message="Недопустимое состояние заказа"):
        super().__init__(message)
