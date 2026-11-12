from .cooking_equipment import CookingEquipment
from culinary.exceptions import KitchenEquipmentError

class Oven(CookingEquipment):
    """Духовой шкаф, расширяющий базовые возможности CookingEquipment."""

    def __init__(self, name, power_watts, status, last_service_days, max_temperature):
        super().__init__(name, power_watts, status, last_service_days)
        if max_temperature <= 0: raise KitchenEquipmentError("Максимальная температура должна быть положительной")
        self.__max_temperature = max_temperature

    @property
    def max_temperature(self): return self.__max_temperature

    def preheat(self, temperature):
        if temperature <= 0 or temperature > self.max_temperature: raise KitchenEquipmentError("Недопустимая температура нагрева")
        self.turn_on()
        return temperature

    def bake(self, minutes):
        if self.status != "включено": raise KitchenEquipmentError("Духовка выключена")
        if minutes <= 0: raise KitchenEquipmentError("Время выпекания должно быть положительным")
        return minutes

    def estimate_energy_kwh(self, minutes):
        if minutes < 0: raise ValueError("Время не может быть отрицательным")
        return self.power_watts * minutes / 60000
