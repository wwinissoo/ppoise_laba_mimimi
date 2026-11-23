from fitness.exceptions import InvalidValueError
from fitness.validation import ensure_number, ensure_text


class HeartRateZone:
    """Пульсовая зона в процентах от максимального пульса."""

    def __init__(self, name, lower_percent, upper_percent):
        self._name = ensure_text(name, "название зоны")
        self._lower_percent = ensure_number(lower_percent, "нижняя граница", 0, 100)
        self._upper_percent = ensure_number(upper_percent, "верхняя граница", 0, 100)
        if self._lower_percent >= self._upper_percent:
            raise InvalidValueError("Нижняя граница зоны должна быть меньше верхней")

    @property
    def name(self):
        return self._name

    @property
    def lower_percent(self):
        return self._lower_percent

    @property
    def upper_percent(self):
        return self._upper_percent

    def bounds(self, max_heart_rate):
        return round(max_heart_rate * self._lower_percent / 100), round(max_heart_rate * self._upper_percent / 100)

    def contains(self, bpm, max_heart_rate):
        lower, upper = self.bounds(max_heart_rate)
        return lower <= bpm < upper
