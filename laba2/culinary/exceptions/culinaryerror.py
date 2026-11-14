from .culinary_exception import CulinaryException


class CulinaryError(CulinaryException):
    """Базовое исключение кулинарной системы."""

    def __init__(self, message="Ошибка кулинарной системы"):
        super().__init__(message)
