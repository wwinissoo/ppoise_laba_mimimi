from culinary.units import MILLIGRAMS_PER_GRAM, PERCENT
from culinary.validation import require_number, require_text


class Nutrient:
    """Нутриент (белки, жиры, витамины…) с суточной нормой потребления."""

    UNITS = {"г": 1, "мг": 0.001, "мкг": 0.000001}
    DEFICIENCY_SHARE = 0.1

    def __init__(self, name, amount_grams, daily_value_grams, unit="г"):
        self.__name = require_text(name, "Название нутриента не может быть пустым")
        self.__amount_grams = require_number(amount_grams, "Количество не может быть отрицательным", minimum=0)
        self.__daily_value_grams = require_number(
            daily_value_grams, "Суточная норма должна быть положительной", positive=True
        )
        if unit not in self.UNITS:
            raise ValueError(f"Единица нутриента должна быть одной из: {', '.join(self.UNITS)}")
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
        """Единица, в которой нутриент принято отображать."""
        return self.__unit

    def daily_value_percentage(self):
        return self.amount_grams / self.daily_value_grams * PERCENT

    def is_deficient(self):
        return self.amount_grams < self.daily_value_grams * self.DEFICIENCY_SHARE

    def convert_to_milligrams(self):
        return self.amount_grams * MILLIGRAMS_PER_GRAM

    def amount_in_display_unit(self):
        return self.amount_grams / self.UNITS[self.unit]
