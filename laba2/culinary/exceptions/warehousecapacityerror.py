from .culinaryerror import CulinaryError

class WarehouseCapacityError(CulinaryError):
    """Превышена вместимость склада."""

    def __init__(self, message="Превышена вместимость склада"):
        super().__init__(message)
