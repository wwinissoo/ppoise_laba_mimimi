"""Сковорода."""
from .kitchen_tool import KitchenTool
class FryingPan(KitchenTool):
    def __init__(self,name,material,condition="исправна",is_clean=True,diameter_cm=24):
        super().__init__(name,material,condition,is_clean)
        if diameter_cm <= 0: raise ValueError("Диаметр должен быть положительным")
        self.__diameter_cm=diameter_cm
    @property
    def diameter_cm(self): return self.__diameter_cm
    def suitable_for_portions(self, portions): return portions > 0 and portions <= max(1,self.diameter_cm//8)
    def recommend_heat(self): return "средний" if self.material.casefold() in ("тефлон","антипригарное покрытие") else "средний или сильный"
