class CookingTime:
    """Объект предметной области: CookingTime."""

    def __init__(self, preparation, cooking, resting, unit):
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
        return self.preparation + self.cooking + self.resting

    def is_quick_recipe(self, limit=30):
        return self.total_minutes() <= limit

    def add_resting_time(self, minutes):
        if minutes < 0: raise ValueError('Время не может быть отрицательным')
        self.__resting += minutes

