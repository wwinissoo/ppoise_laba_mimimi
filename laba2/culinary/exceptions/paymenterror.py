from .culinaryerror import CulinaryError

class PaymentError(CulinaryError):
    """Ошибка оплаты."""

    def __init__(self, message="Ошибка оплаты"):
        super().__init__(message)
