"""Описание подачи готового блюда."""

from culinary.exceptions import InvalidTemperatureException, PortionException
from culinary.validation import is_number


class Serving:
    """Хранит параметры подачи блюда."""

    MIN_TEMPERATURE = -20
    MAX_TEMPERATURE = 150

    def __init__(self, temperature_celsius, presentation, serving_size_grams):
        if not is_number(temperature_celsius) or not (
            self.MIN_TEMPERATURE <= temperature_celsius <= self.MAX_TEMPERATURE
        ):
            raise InvalidTemperatureException("Недопустимая температура подачи")
        if not is_number(serving_size_grams) or serving_size_grams <= 0:
            raise PortionException("Размер порции должен быть положительным")
        self.__temperature_celsius = temperature_celsius
        self.__presentation = str(presentation).strip()
        self.__serving_size_grams = serving_size_grams

    @property
    def temperature_celsius(self):
        return self.__temperature_celsius

    @property
    def presentation(self):
        return self.__presentation

    @property
    def serving_size_grams(self):
        return self.__serving_size_grams

    def describe(self):
        return f"Подача: {self.presentation}; {self.serving_size_grams} г; {self.temperature_celsius} °C"

    def calculate_total_weight(self, portions):
        if not isinstance(portions, int) or portions <= 0:
            raise PortionException("Количество порций должно быть положительным")
        return self.serving_size_grams * portions
