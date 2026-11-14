from culinary.units import GRAMS_PER_KILOGRAM, PERCENT
from culinary.exceptions import (
    InvalidIngredientError,
    InsufficientIngredientError,
    ExpiredIngredientError,
    InvalidTemperatureException,
)
from culinary.validation import is_number, require_number, require_positive_int, require_text


class Ingredient:
    """Базовый ингредиент: хранит количество, цену, пищевую ценность и срок годности."""

    GRAMS_PER_KILOGRAM = GRAMS_PER_KILOGRAM
    CALORIE_REFERENCE_GRAMS = 100
    MIN_STORAGE_TEMPERATURE = -40
    MAX_STORAGE_TEMPERATURE = 40

    def __init__(
        self,
        name,
        weight,
        price_per_kg,
        calories,
        expiration_days,
        storage_temperature,
        allow_zero=False,
    ):
        name = require_text(name, "Название ингредиента не может быть пустым", InvalidIngredientError)
        if not is_number(weight) or weight < 0 or (weight == 0 and not allow_zero):
            raise InvalidIngredientError("Вес ингредиента должен быть положительным")
        require_number(price_per_kg, "Цена за килограмм не может быть отрицательной", InvalidIngredientError, 0)
        require_number(calories, "Калорийность не может быть отрицательной", InvalidIngredientError, 0)
        require_positive_int(
            expiration_days, "Срок годности должен быть положительным целым числом", InvalidIngredientError
        )
        self._validate_storage_temperature(storage_temperature)
        self.__name = name
        self.__initial_weight = weight
        self.__weight = weight
        self.__price_per_kg = price_per_kg
        self.__calories = calories
        self.__expiration_days = expiration_days
        self.__storage_temperature = storage_temperature
        self.__is_available = weight > 0
        self.__days_passed = 0

    @classmethod
    def _validate_storage_temperature(cls, temperature):
        if not is_number(temperature):
            raise InvalidIngredientError("Температура хранения должна быть числом")
        if not cls.MIN_STORAGE_TEMPERATURE <= temperature <= cls.MAX_STORAGE_TEMPERATURE:
            raise InvalidTemperatureException(
                f"Температура хранения должна быть от {cls.MIN_STORAGE_TEMPERATURE} "
                f"до {cls.MAX_STORAGE_TEMPERATURE} °C"
            )

    @property
    def name(self):
        return self.__name

    @property
    def weight(self):
        return self.__weight

    @property
    def price_per_kg(self):
        return self.__price_per_kg

    @property
    def calories(self):
        return self.__calories

    @property
    def expiration_days(self):
        return self.__expiration_days

    @property
    def storage_temperature(self):
        return self.__storage_temperature

    @property
    def is_available(self):
        return self.__is_available

    @property
    def initial_weight(self):
        return self.__initial_weight

    @property
    def days_passed(self):
        return self.__days_passed

    def calculate_cost(self, amount):
        """Стоимость amount граммов по текущей цене; от остатка партии не зависит."""
        require_number(
            amount, "Количество для расчёта должно быть положительным", InvalidIngredientError, positive=True
        )
        return self.__price_per_kg * amount / self.GRAMS_PER_KILOGRAM

    def calculate_calories(self, amount):
        require_number(amount, "Количество не может быть отрицательным", InvalidIngredientError, 0)
        return self.__calories * amount / self.CALORIE_REFERENCE_GRAMS

    def consume(self, amount):
        require_number(
            amount, "Количество для расходования должно быть положительным", InvalidIngredientError, positive=True
        )
        if amount > self.__weight:
            raise InsufficientIngredientError(f"Недостаточно ингредиента «{self.name}»")
        self.__weight -= amount
        if self.__weight == 0:
            self.__is_available = False

    def receive(self, amount):
        require_number(
            amount, "Количество поступления должно быть положительным", InvalidIngredientError, positive=True
        )
        self.require_fresh()
        if self.__initial_weight == 0:
            self.__initial_weight = amount
        self.__weight += amount
        self.__is_available = True

    def check_expiration(self):
        return self.__days_passed < self.__expiration_days

    def require_fresh(self):
        if not self.check_expiration():
            raise ExpiredIngredientError(f"Ингредиент «{self.name}» просрочен")
        return True

    def pass_day(self):
        self.__days_passed += 1
        if not self.check_expiration():
            self.__is_available = False

    def calculate_remaining_percentage(self):
        if self.__initial_weight == 0:
            return 0
        return self.__weight / self.__initial_weight * PERCENT

    def update_price(self, new_price):
        require_number(new_price, "Цена не может быть отрицательной", InvalidIngredientError, 0)
        self.__price_per_kg = new_price

    def update_storage_temperature(self, new_temperature):
        self._validate_storage_temperature(new_temperature)
        self.__storage_temperature = new_temperature
