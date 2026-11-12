from ingredient import Ingredient

class Oil(Ingredient):
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 smoke_point=200, is_refined=True, oil_type="растительное"):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if smoke_point <= 0:
            raise ValueError("Температура дымления должна быть положительной")
        self.__smoke_point = smoke_point
        self.__is_refined = bool(is_refined)
        self.__oil_type = oil_type
        self.__is_heated = False

    @property
    def smoke_point(self): return self.__smoke_point
    @property
    def is_refined(self): return self.__is_refined
    @property
    def oil_type(self): return self.__oil_type
    @property
    def is_heated(self): return self.__is_heated

    def heat(self, temperature):
        if temperature <= 0 or temperature > self.__smoke_point:
            raise ValueError("Температура выходит за допустимый диапазон")
        self.__is_heated = True
        return temperature

    def is_suitable_for_frying(self, required_temperature):
        return self.__smoke_point >= required_temperature

    def calculate_remaining_after_frying(self, used_amount):
        if used_amount < 0 or used_amount > self.weight:
            raise ValueError("Некорректное использованное количество")
        return self.weight - used_amount

    def classify_refinement(self):
        return "рафинированное" if self.__is_refined else "нерафинированное"
