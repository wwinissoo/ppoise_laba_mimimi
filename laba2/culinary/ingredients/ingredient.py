from culinary.exceptions import InvalidIngredientError, InsufficientIngredientError, ExpiredIngredientError

class Ingredient:
    """Базовый ингредиент: хранит количество, цену, пищевую ценность и срок годности."""

    GRAMS_PER_KILOGRAM = 1000
    CALORIE_REFERENCE_GRAMS = 100

    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature):
        if not isinstance(name, str) or not name.strip():
            raise InvalidIngredientError("Название ингредиента не может быть пустым")
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise InvalidIngredientError("Вес ингредиента должен быть положительным")
        if not isinstance(price_per_kg, (int, float)) or price_per_kg < 0:
            raise InvalidIngredientError("Цена за килограмм не может быть отрицательной")
        if not isinstance(calories, (int, float)) or calories < 0:
            raise InvalidIngredientError("Калорийность не может быть отрицательной")
        if not isinstance(expiration_days, int) or expiration_days <= 0:
            raise InvalidIngredientError("Срок годности должен быть положительным целым числом")
        if not isinstance(storage_temperature, (int, float)):
            raise InvalidIngredientError("Температура хранения должна быть числом")
        self.__name = name.strip()
        self.__initial_weight = weight
        self.__weight = weight
        self.__price_per_kg = price_per_kg
        self.__calories = calories
        self.__expiration_days = expiration_days
        self.__storage_temperature = storage_temperature
        self.__is_available = True
        self.__days_passed = 0

    @property
    def name(self): return self.__name
    @property
    def weight(self): return self.__weight
    @property
    def price_per_kg(self): return self.__price_per_kg
    @property
    def calories(self): return self.__calories
    @property
    def expiration_days(self): return self.__expiration_days
    @property
    def storage_temperature(self): return self.__storage_temperature
    @property
    def is_available(self): return self.__is_available
    @property
    def initial_weight(self): return self.__initial_weight
    @property
    def days_passed(self): return self.__days_passed

    def calculate_cost(self, amount):
        if amount <= 0:
            raise InvalidIngredientError("Количество для расчёта должно быть положительным")
        if amount > self.__weight:
            raise InsufficientIngredientError(f"Недостаточно ингредиента «{self.name}»")
        return self.__price_per_kg * amount / self.GRAMS_PER_KILOGRAM

    def calculate_calories(self, amount):
        if amount < 0:
            raise InvalidIngredientError("Количество не может быть отрицательным")
        return self.__calories * amount / self.CALORIE_REFERENCE_GRAMS

    def consume(self, amount):
        if amount <= 0:
            raise InvalidIngredientError("Количество для расходования должно быть положительным")
        if amount > self.__weight:
            raise InsufficientIngredientError(f"Недостаточно ингредиента «{self.name}»")
        self.__weight -= amount
        if self.__weight == 0:
            self.__is_available = False

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
        return self.__weight / self.__initial_weight * 100

    def update_price(self, new_price):
        if new_price < 0:
            raise InvalidIngredientError("Цена не может быть отрицательной")
        self.__price_per_kg = new_price

    def update_storage_temperature(self, new_temperature):
        if not isinstance(new_temperature, (int, float)):
            raise InvalidIngredientError("Температура хранения должна быть числом")
        self.__storage_temperature = new_temperature
