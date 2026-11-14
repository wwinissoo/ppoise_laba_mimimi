from culinary.units import MINUTES_PER_HOUR
from culinary.exceptions import CookingTimeException
from culinary.validation import require_number


class CookingTime:
    """Время подготовки, термообработки и отдыха блюда."""

    UNITS = {"мин": 1, "ч": MINUTES_PER_HOUR}
    QUICK_RECIPE_MINUTES = 30

    def __init__(self, preparation, cooking, resting, unit="мин"):
        for value in (preparation, cooking, resting):
            require_number(value, "Время не может быть отрицательным", CookingTimeException, 0)
        if unit not in self.UNITS:
            raise CookingTimeException("Единица времени должна быть «мин» или «ч»")
        self.__preparation = preparation
        self.__cooking = cooking
        self.__resting = resting
        self.__unit = unit

    @property
    def preparation(self):
        return self.__preparation

    @property
    def cooking(self):
        return self.__cooking

    @property
    def resting(self):
        return self.__resting

    @property
    def unit(self):
        return self.__unit

    def total_minutes(self):
        return (self.preparation + self.cooking + self.resting) * self.UNITS[self.unit]

    def is_quick_recipe(self, limit=QUICK_RECIPE_MINUTES):
        return self.total_minutes() <= limit

    def add_resting_time(self, minutes):
        require_number(minutes, "Время не может быть отрицательным", CookingTimeException, 0)
        self.__resting += minutes / self.UNITS[self.unit]
