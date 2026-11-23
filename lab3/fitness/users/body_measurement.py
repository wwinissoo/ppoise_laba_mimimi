from datetime import date

from fitness.exceptions import InvalidMeasurementError, InvalidValueError
from fitness.validation import ensure_instance, ensure_number


class BodyMeasurement:
    """Замер тела на определённую дату."""

    UNDERWEIGHT_LIMIT = 18.5
    NORMAL_LIMIT = 25
    OVERWEIGHT_LIMIT = 30
    CM_IN_METER = 100

    def __init__(self, measured_on, weight_kg, height_cm, body_fat_percent=None, waist_cm=None):
        self._measured_on = ensure_instance(measured_on, date, "дата замера")
        self._weight_kg = self._physical(weight_kg, "вес", 20, 400)
        self._height_cm = self._physical(height_cm, "рост", 50, 260)
        self._body_fat_percent = None if body_fat_percent is None else self._physical(body_fat_percent, "% жира", 2, 70)
        self._waist_cm = None if waist_cm is None else self._physical(waist_cm, "талия", 30, 250)

    @staticmethod
    def _physical(value, field_name, minimum, maximum):
        try:
            return ensure_number(value, field_name, minimum, maximum)
        except InvalidValueError as error:
            raise InvalidMeasurementError(str(error)) from None

    @property
    def measured_on(self):
        return self._measured_on

    @property
    def weight_kg(self):
        return self._weight_kg

    @property
    def height_cm(self):
        return self._height_cm

    @property
    def body_fat_percent(self):
        return self._body_fat_percent

    @property
    def waist_cm(self):
        return self._waist_cm

    def bmi(self):
        height_m = self._height_cm / self.CM_IN_METER
        return round(self._weight_kg / height_m**2, 1)

    def bmi_category(self):
        value = self.bmi()
        if value < self.UNDERWEIGHT_LIMIT:
            return "дефицит массы"
        if value < self.NORMAL_LIMIT:
            return "норма"
        if value < self.OVERWEIGHT_LIMIT:
            return "избыточный вес"
        return "ожирение"

    def lean_mass_kg(self):
        if self._body_fat_percent is None:
            raise InvalidMeasurementError("Для расчёта сухой массы нужен процент жира")
        return round(self._weight_kg * (1 - self._body_fat_percent / 100), 1)

    def waist_to_height_ratio(self):
        if self._waist_cm is None:
            raise InvalidMeasurementError("Не указан обхват талии")
        return round(self._waist_cm / self._height_cm, 2)

    def weight_difference(self, earlier):
        ensure_instance(earlier, BodyMeasurement, "предыдущий замер")
        return round(self._weight_kg - earlier.weight_kg, 1)
