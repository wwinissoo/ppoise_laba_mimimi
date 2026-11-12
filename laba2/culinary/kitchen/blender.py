"""Блендер."""
from .cooking_equipment import CookingEquipment
class Blender(CookingEquipment):
    def __init__(self,name,power_watts,status="выключено",last_service_days=0,max_speed=5):
        super().__init__(name,power_watts,status,last_service_days)
        if max_speed <= 0: raise ValueError("Скорость должна быть положительной")
        self.__max_speed=max_speed
    @property
    def max_speed(self): return self.__max_speed
    def validate_speed(self,speed): return isinstance(speed,int) and 1 <= speed <= self.max_speed
    def blend_time(self, ingredients_count):
        if ingredients_count <= 0: raise ValueError("Количество ингредиентов должно быть положительным")
        return ingredients_count * 15
