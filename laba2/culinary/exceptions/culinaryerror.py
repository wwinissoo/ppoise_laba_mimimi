class CulinaryError(Exception):
    """Базовое исключение кулинарной системы."""

    def __init__(self, message="Ошибка кулинарной системы"):
        super().__init__(message)
