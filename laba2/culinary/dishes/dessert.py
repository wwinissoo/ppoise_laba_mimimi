"""Десерт."""

from culinary.validation import require_number
from .dish import Dish


class Dessert(Dish):
    """Десерт с содержанием сахара; может подаваться охлаждённым."""

    CHILLED_TEMPERATURE = 6
    ROOM_TEMPERATURE = 20
    LOW_SUGAR_GRAMS = 10

    def __init__(self, name, recipe, portions, serving_temperature=ROOM_TEMPERATURE, sugar_grams=0, chilled=False):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__sugar_grams = require_number(sugar_grams, "Сахар не может быть отрицательным", minimum=0)
        self.__chilled = False
        if chilled:
            self.chill()

    @property
    def sugar_grams(self):
        return self.__sugar_grams

    @property
    def chilled(self):
        return self.__chilled

    def calculate_sugar_per_portion(self):
        return self.sugar_grams / self.portions

    def is_low_sugar(self, limit=LOW_SUGAR_GRAMS):
        return self.calculate_sugar_per_portion() <= limit

    def chill(self):
        self.change_serving_temperature(min(self.serving_temperature, self.CHILLED_TEMPERATURE))
        self.__chilled = True
