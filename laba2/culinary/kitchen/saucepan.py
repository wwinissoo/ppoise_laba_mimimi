"""Кастрюля."""

from culinary.units import PERCENT
from culinary.exceptions import KitchenEquipmentError
from culinary.validation import require_number
from .kitchen_tool import KitchenTool


class Saucepan(KitchenTool):
    def __init__(self, name, material, condition="исправен", is_clean=True, capacity_liters=2.0):
        super().__init__(name, material, condition, is_clean)
        self.__capacity_liters = require_number(
            capacity_liters, "Объём должен быть положительным", KitchenEquipmentError, positive=True
        )

    @property
    def capacity_liters(self):
        return self.__capacity_liters

    def can_hold(self, volume_liters):
        return 0 <= volume_liters <= self.capacity_liters

    def fill_percentage(self, volume_liters):
        require_number(volume_liters, "Объём не может быть отрицательным", minimum=0)
        return volume_liters / self.capacity_liters * PERCENT
