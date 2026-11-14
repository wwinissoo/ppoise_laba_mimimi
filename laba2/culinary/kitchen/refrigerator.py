from culinary.units import HOURS_PER_DAY, WATTS_PER_KILOWATT
from .cooking_equipment import CookingEquipment
from culinary.exceptions import InvalidTemperatureException
from culinary.validation import is_number


class Refrigerator(CookingEquipment):
    """Холодильник с дополнительным параметром температуры."""

    MIN_TEMPERATURE = -30
    MAX_TEMPERATURE = 10
    STORAGE_TOLERANCE = 2

    def __init__(self, name, power_watts, status, last_service_days, temperature):
        super().__init__(name, power_watts, status, last_service_days)
        self._validate_temperature(temperature)
        self.__temperature = temperature

    @classmethod
    def _validate_temperature(cls, temperature):
        if not is_number(temperature) or not cls.MIN_TEMPERATURE <= temperature <= cls.MAX_TEMPERATURE:
            raise InvalidTemperatureException("Температура холодильника вне допустимого диапазона")

    @property
    def temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self._validate_temperature(temperature)
        self.__temperature = temperature

    def is_freezing(self):
        return self.__temperature <= 0

    def can_store(self, ingredient):
        """Подходит ли холодильник для хранения ингредиента (допуск ±2 °C)."""
        return (
            self.is_operational() and abs(ingredient.storage_temperature - self.__temperature) <= self.STORAGE_TOLERANCE
        )

    def estimate_daily_energy(self):
        return self.power_watts * HOURS_PER_DAY / WATTS_PER_KILOWATT
