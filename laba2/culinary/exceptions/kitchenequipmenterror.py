from .culinaryerror import CulinaryError

class KitchenEquipmentError(CulinaryError):
    """Ошибка кухонного оборудования."""

    def __init__(self, message="Ошибка кухонного оборудования"):
        super().__init__(message)
