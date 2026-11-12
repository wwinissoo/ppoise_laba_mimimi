from ingredient import Ingredient

class Vegetable(Ingredient):
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 is_organic=False, requires_peeling=False, water_percentage=90):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not 0 <= water_percentage <= 100:
            raise ValueError("Содержание воды должно быть от 0 до 100")
        self.__is_organic = bool(is_organic)
        self.__requires_peeling = bool(requires_peeling)
        self.__water_percentage = water_percentage
        self.__is_washed = False
        self.__is_peeled = False

    @property
    def is_organic(self): return self.__is_organic
    @property
    def requires_peeling(self): return self.__requires_peeling
    @property
    def water_percentage(self): return self.__water_percentage
    @property
    def is_washed(self): return self.__is_washed
    @property
    def is_peeled(self): return self.__is_peeled

    def wash(self):
        self.__is_washed = True
        return self.name

    def peel(self):
        if not self.__requires_peeling:
            return False
        self.__is_peeled = True
        return True

    def calculate_clean_weight(self, waste_percentage):
        if not 0 <= waste_percentage < 100:
            raise ValueError("Потери должны быть от 0 до 100 процентов")
        return self.weight * (100 - waste_percentage) / 100

    def is_suitable_for_salad(self):
        return self.__is_washed and self.is_available
