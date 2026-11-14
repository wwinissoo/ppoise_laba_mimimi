from .culinaryerror import CulinaryError
from .payment_exception import PaymentException


class PaymentError(CulinaryError, PaymentException):
    """Ошибка оплаты."""

    def __init__(self, message="Ошибка оплаты"):
        super().__init__(message)
