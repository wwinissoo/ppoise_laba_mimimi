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
        if not name:
            raise ValueError("Название ингредиента не может быть пустым")

        if weight <= 0:
            raise ValueError("Вес должен быть положительным")

        if price_per_kg < 0:
            raise ValueError("Цена не может быть отрицательной")

        if calories < 0:
            raise ValueError("Калорийность не может быть отрицательной")

        if expiration_days <= 0:
            raise ValueError("Срок годности должен быть положительным")

        self.name = name
        self.weight = weight
        self.price_per_kg = price_per_kg
        self.calories = calories
        self.expiration_days = expiration_days
        self.storage_temperature = storage_temperature
        self.is_available = True

    def calculate_cost(self, amount):
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")

        if amount > self.weight:
            raise ValueError("Недостаточно ингредиента")

        return self.price_per_kg * amount / 1000

    def calculate_calories(self, amount):
        if amount < 0:
            raise ValueError("Количество не может быть отрицательным")

        return self.calories * amount / 100

    def consume(self, amount):
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")

        if amount > self.weight:
            raise ValueError("Недостаточно ингредиента")

        self.weight -= amount

        if self.weight == 0:
            self.is_available = False

    def check_expiration(self, days_passed):
        if days_passed < 0:
            raise ValueError("Количество дней не может быть отрицательным")

        return days_passed < self.expiration_days

    def calculate_remaining_percentage(self, used_weight):
        if used_weight < 0 or used_weight > self.weight:
            raise ValueError("Некорректное количество")

        if self.weight == 0:
            return 0

        return (self.weight - used_weight) / self.weight * 100
