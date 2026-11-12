
class Ingredient:
    def __init__(
        self,
        name,
        weight,
        price_per_kg,
        calories,
        expiration_days,
        storage_temperature
    ):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название не может быть пустым")

        if weight <= 0:
            raise ValueError("Вес должен быть положительным")

        if price_per_kg < 0:
            raise ValueError("Цена не может быть отрицательной")

        if calories < 0:
            raise ValueError("Калорийность не может быть отрицательной")

        if expiration_days <= 0:
            raise ValueError("Срок годности должен быть положительным")

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

    def calculate_cost(self, amount):
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")

        if amount > self.__weight:
            raise ValueError("Недостаточно ингредиента")

        return self.__price_per_kg * amount / 1000

    def calculate_calories(self, amount):
        if amount < 0:
            raise ValueError("Количество не может быть отрицательным")

        return self.__calories * amount / 100

    def consume(self, amount):
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")

        if amount > self.__weight:
            raise ValueError("Недостаточно ингредиента")

        self.__weight -= amount

        if self.__weight == 0:
            self.__is_available = False

    def check_expiration(self):
        return self.__days_passed < self.__expiration_days

    def pass_day(self):
        self.__days_passed += 1

    def calculate_remaining_percentage(self):
        if self.__initial_weight == 0:
            return 0

        return self.__weight / self.__initial_weight * 100

    def update_price(self, new_price):
        if new_price < 0:
            raise ValueError("Цена не может быть отрицательной")

        self.__price_per_kg = new_price

    def update_storage_temperature(self, new_temperature):
        self.__storage_temperature = new_temperature
