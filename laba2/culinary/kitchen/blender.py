"""Блендер."""

from culinary.exceptions import KitchenEquipmentError
from culinary.validation import require_number, require_positive_int
from .cooking_equipment import CookingEquipment


class Blender(CookingEquipment):
    SECONDS_PER_INGREDIENT = 15
    DEFAULT_MAX_SPEED = 5

    def __init__(self, name, power_watts, status="выключено", last_service_days=0, max_speed=DEFAULT_MAX_SPEED):
        super().__init__(name, power_watts, status, last_service_days)
        require_positive_int(max_speed, "Скорость должна быть положительным целым числом", KitchenEquipmentError)
        self.__max_speed = max_speed

    @property
    def max_speed(self):
        return self.__max_speed

    def validate_speed(self, speed):
        return isinstance(speed, int) and not isinstance(speed, bool) and 1 <= speed <= self.max_speed

    def blend_time(self, ingredients_count):
        require_number(
            ingredients_count, "Количество ингредиентов должно быть положительным", KitchenEquipmentError, positive=True
        )
        return ingredients_count * self.SECONDS_PER_INGREDIENT
