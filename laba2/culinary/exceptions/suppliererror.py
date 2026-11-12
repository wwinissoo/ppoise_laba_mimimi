from .culinaryerror import CulinaryError

class SupplierError(CulinaryError):
    """Ошибка поставщика."""

    def __init__(self, message="Ошибка поставщика"):
        super().__init__(message)
