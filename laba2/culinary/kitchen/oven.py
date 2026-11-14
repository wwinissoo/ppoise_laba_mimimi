from culinary.units import MINUTES_PER_HOUR, WATTS_PER_KILOWATT
from .cooking_equipment import CookingEquipment
from culinary.exceptions import CookingTimeException, InvalidTemperatureException, KitchenEquipmentError
from culinary.validation import is_number, require_number


class Oven(CookingEquipment):
    """Духовой шкаф, расширяющий базовые возможности CookingEquipment."""

    def __init__(self, name, power_watts, status, last_service_days, max_temperature):
        super().__init__(name, power_watts, status, last_service_days)
        require_number(
            max_temperature, "Максимальная температура должна быть положительной", KitchenEquipmentError, positive=True
        )
        self.__max_temperature = max_temperature
        self.__current_temperature = 0

    @property
    def max_temperature(self):
        return self.__max_temperature

    @property
    def current_temperature(self):
        return self.__current_temperature

    def preheat(self, temperature):
        if not is_number(temperature) or temperature <= 0 or temperature > self.max_temperature:
            raise InvalidTemperatureException("Недопустимая температура нагрева")
        self.turn_on()
        self.__current_temperature = temperature
        return temperature

    def bake(self, minutes):
        if self.status != "включено" or self.__current_temperature == 0:
            raise KitchenEquipmentError("Духовка не разогрета")
        require_number(minutes, "Время выпекания должно быть положительным", CookingTimeException, positive=True)
        return minutes

    def turn_off(self):
        super().turn_off()
        self.__current_temperature = 0

    def estimate_energy_kwh(self, minutes):
        require_number(minutes, "Время не может быть отрицательным", CookingTimeException, 0)
        return self.power_watts * minutes / MINUTES_PER_HOUR / WATTS_PER_KILOWATT
