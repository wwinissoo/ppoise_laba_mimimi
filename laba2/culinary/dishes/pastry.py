"""Класс выпечки."""

from culinary.exceptions import CookingTimeException, InvalidTemperatureException
from culinary.validation import is_number
from .dish import Dish


class Pastry(Dish):
    """Выпечка с температурой выпекания и временем в духовке."""

    MAX_BAKING_TEMPERATURE = 300

    def __init__(self, name, recipe, portions, serving_temperature, baking_temperature, baking_minutes):
        super().__init__(name, recipe, portions, serving_temperature)
        if not is_number(baking_temperature) or not 0 < baking_temperature <= self.MAX_BAKING_TEMPERATURE:
            raise InvalidTemperatureException(
                f"Температура выпекания должна быть от 0 до {self.MAX_BAKING_TEMPERATURE} °C"
            )
        if not is_number(baking_minutes) or baking_minutes <= 0:
            raise CookingTimeException("Время выпекания должно быть положительным")
        self.__baking_temperature = baking_temperature
        self.__baking_minutes = baking_minutes

    @property
    def baking_temperature(self):
        return self.__baking_temperature

    @property
    def baking_minutes(self):
        return self.__baking_minutes

    def estimate_baking_end(self, start_minute):
        if not is_number(start_minute) or start_minute < 0:
            raise CookingTimeException("Минута начала не может быть отрицательной")
        return start_minute + self.baking_minutes

    def can_bake_in(self, oven):
        """Проверяет, что духовка исправна и разогревается до нужной температуры."""
        from culinary.kitchen.oven import Oven

        if not isinstance(oven, Oven):
            raise TypeError("Ожидается объект Oven")
        return oven.status != "неисправно" and oven.max_temperature >= self.baking_temperature
