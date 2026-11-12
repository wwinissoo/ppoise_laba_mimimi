from culinary.exceptions import KitchenEquipmentError

class CookingEquipment:
    """Базовый класс кухонного оборудования."""

    VALID_STATUSES = {"выключено", "включено", "неисправно"}

    def __init__(self, name, power_watts, status, last_service_days):
        if not isinstance(name, str) or not name.strip(): raise KitchenEquipmentError("Название оборудования обязательно")
        if power_watts < 0 or last_service_days < 0: raise KitchenEquipmentError("Мощность и срок после обслуживания не могут быть отрицательными")
        if status not in self.VALID_STATUSES: raise KitchenEquipmentError("Неизвестный статус оборудования")
        self.__name = name.strip()
        self.__power_watts = power_watts
        self.__status = status
        self.__last_service_days = last_service_days

    @property
    def name(self): return self.__name
    @property
    def power_watts(self): return self.__power_watts
    @property
    def status(self): return self.__status
    @property
    def last_service_days(self): return self.__last_service_days

    def turn_on(self):
        if self.__status == "неисправно": raise KitchenEquipmentError("Нельзя включить неисправное оборудование")
        self.__status = "включено"

    def turn_off(self):
        self.__status = "выключено"

    def needs_service(self, interval):
        if interval < 0: raise ValueError("Интервал обслуживания не может быть отрицательным")
        return self.__last_service_days >= interval

    def record_service(self):
        self.__last_service_days = 0
        if self.__status == "неисправно": self.__status = "выключено"
