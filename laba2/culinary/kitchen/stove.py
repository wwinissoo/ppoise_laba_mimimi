"""Плита."""
from .cooking_equipment import CookingEquipment
class Stove(CookingEquipment):
    def __init__(self, name, power_watts, status="выключено", last_service_days=0, burner_count=4):
        super().__init__(name,power_watts,status,last_service_days)
        if burner_count <= 0: raise ValueError("Количество конфорок должно быть положительным")
        self.__burner_count=burner_count
    @property
    def burner_count(self): return self.__burner_count
    def can_use_burners(self, requested): return 0 < requested <= self.burner_count
    def estimate_energy(self, minutes):
        if minutes < 0: raise ValueError("Время не может быть отрицательным")
        return self.power_watts * minutes / 60 / 1000
