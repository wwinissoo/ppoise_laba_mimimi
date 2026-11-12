from ingredient import Ingredient

class DairyProduct(Ingredient):
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 fat_percentage=3.2, lactose_free=False, fermentation_required=False):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not 0 <= fat_percentage <= 100:
            raise ValueError("Жирность должна быть от 0 до 100")
        self.__fat_percentage = fat_percentage
        self.__lactose_free = bool(lactose_free)
        self.__fermentation_required = bool(fermentation_required)
        self.__is_fermented = False

    @property
    def fat_percentage(self): return self.__fat_percentage
    @property
    def lactose_free(self): return self.__lactose_free
    @property
    def fermentation_required(self): return self.__fermentation_required
    @property
    def is_fermented(self): return self.__is_fermented

    def ferment(self, hours):
        if hours <= 0:
            raise ValueError("Время ферментации должно быть положительным")
        if not self.__fermentation_required:
            return False
        self.__is_fermented = True
        return hours

    def calculate_fat_weight(self):
        return self.weight * self.__fat_percentage / 100

    def is_suitable_for_lactose_free_diet(self):
        return self.__lactose_free

    def check_fermentation(self):
        return not self.__fermentation_required or self.__is_fermented
