"""Сковорода."""

from culinary.exceptions import KitchenEquipmentError
from culinary.validation import require_number
from .kitchen_tool import KitchenTool


class FryingPan(KitchenTool):
    NON_STICK_MATERIALS = ("тефлон", "антипригарное покрытие")
    CM_PER_PORTION = 8
    DEFAULT_DIAMETER_CM = 24

    def __init__(self, name, material, condition="исправен", is_clean=True, diameter_cm=DEFAULT_DIAMETER_CM):
        super().__init__(name, material, condition, is_clean)
        self.__diameter_cm = require_number(
            diameter_cm, "Диаметр должен быть положительным", KitchenEquipmentError, positive=True
        )

    @property
    def diameter_cm(self):
        return self.__diameter_cm

    def suitable_for_portions(self, portions):
        return 0 < portions <= max(1, self.diameter_cm // self.CM_PER_PORTION)

    def recommend_heat(self):
        return "средний" if self.material.casefold() in self.NON_STICK_MATERIALS else "средний или сильный"
