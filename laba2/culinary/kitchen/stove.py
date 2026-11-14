"""Плита."""

from culinary.units import MINUTES_PER_HOUR, WATTS_PER_KILOWATT
from culinary.exceptions import KitchenEquipmentError
from culinary.validation import require_number, require_positive_int
from .cooking_equipment import CookingEquipment


class Stove(CookingEquipment):
    DEFAULT_BURNERS = 4

    def __init__(self, name, power_watts, status="выключено", last_service_days=0, burner_count=DEFAULT_BURNERS):
        super().__init__(name, power_watts, status, last_service_days)
        require_positive_int(
            burner_count, "Количество конфорок должно быть положительным целым числом", KitchenEquipmentError
        )
        self.__burner_count = burner_count

    @property
    def burner_count(self):
        return self.__burner_count

    def can_use_burners(self, requested):
        return self.is_operational() and 0 < requested <= self.burner_count

    def estimate_energy(self, minutes):
        require_number(minutes, "Время не может быть отрицательным", minimum=0)
        return self.power_watts * minutes / MINUTES_PER_HOUR / WATTS_PER_KILOWATT
