class Nutrient:
    """Объект предметной области: Nutrient."""

    def __init__(self, name, amount_grams, daily_value_grams, unit):
        self.__name = name
        self.__amount_grams = amount_grams
        self.__daily_value_grams = daily_value_grams
        self.__unit = unit

    @property
    def name(self):
        return self.__name

    @property
    def amount_grams(self):
        return self.__amount_grams

    @property
    def daily_value_grams(self):
        return self.__daily_value_grams

    @property
    def unit(self):
        return self.__unit

    def daily_value_percentage(self):
        if self.daily_value_grams <= 0: return 0
        return self.amount_grams / self.daily_value_grams * 100

    def is_deficient(self):
        return self.amount_grams < self.daily_value_grams * 0.1

    def convert_to_milligrams(self):
        return self.amount_grams * 1000

