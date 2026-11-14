from culinary.exceptions import KitchenEquipmentError
from culinary.validation import require_number, require_text


class CookingEquipment:
    """Базовый класс кухонного оборудования."""

    VALID_STATUSES = {"выключено", "включено", "неисправно"}

    def __init__(self, name, power_watts, status="выключено", last_service_days=0):
        self.__name = require_text(name, "Название оборудования обязательно", KitchenEquipmentError)
        require_number(power_watts, "Мощность не может быть отрицательной", KitchenEquipmentError, 0)
        require_number(
            last_service_days, "Срок после обслуживания не может быть отрицательным", KitchenEquipmentError, 0
        )
        if status not in self.VALID_STATUSES:
            raise KitchenEquipmentError("Неизвестный статус оборудования")
        self.__power_watts = power_watts
        self.__status = status
        self.__last_service_days = last_service_days

    @property
    def name(self):
        return self.__name

    @property
    def power_watts(self):
        return self.__power_watts

    @property
    def status(self):
        return self.__status

    @property
    def last_service_days(self):
        return self.__last_service_days

    def is_operational(self):
        return self.__status != "неисправно"

    def turn_on(self):
        if not self.is_operational():
            raise KitchenEquipmentError("Нельзя включить неисправное оборудование")
        self.__status = "включено"

    def turn_off(self):
        if self.is_operational():
            self.__status = "выключено"

    def mark_broken(self):
        self.__status = "неисправно"

    def pass_days(self, days=1):
        require_number(days, "Количество дней должно быть положительным", KitchenEquipmentError, positive=True)
        self.__last_service_days += days

    def needs_service(self, interval):
        require_number(interval, "Интервал обслуживания не может быть отрицательным", minimum=0)
        return self.__last_service_days >= interval

    def record_service(self):
        self.__last_service_days = 0
        if self.__status == "неисправно":
            self.__status = "выключено"
