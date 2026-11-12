from .cooking_equipment import CookingEquipment
from culinary.exceptions import KitchenEquipmentError

class Refrigerator(CookingEquipment):
    """Холодильник с дополнительным параметром температуры."""

    def __init__(self, name, power_watts, status, last_service_days, temperature):
        super().__init__(name, power_watts, status, last_service_days)
        self.__temperature = temperature

    @property
    def temperature(self): return self.__temperature

    def set_temperature(self, temperature):
        if temperature > 10 or temperature < -30: raise KitchenEquipmentError("Температура холодильника вне допустимого диапазона")
        self.__temperature = temperature

    def is_freezing(self):
        return self.__temperature <= 0

    def estimate_daily_energy(self):
        return self.power_watts * 24 / 1000
