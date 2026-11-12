"""Кастрюля."""
from .kitchen_tool import KitchenTool
class Saucepan(KitchenTool):
    def __init__(self,name,material,condition="исправна",is_clean=True,capacity_liters=2.0):
        super().__init__(name,material,condition,is_clean)
        if capacity_liters <= 0: raise ValueError("Объём должен быть положительным")
        self.__capacity_liters=capacity_liters
    @property
    def capacity_liters(self): return self.__capacity_liters
    def can_hold(self, volume_liters): return 0 <= volume_liters <= self.capacity_liters
    def fill_percentage(self, volume_liters):
        if volume_liters < 0: raise ValueError("Объём не может быть отрицательным")
        return volume_liters/self.capacity_liters*100
