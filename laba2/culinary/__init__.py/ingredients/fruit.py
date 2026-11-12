from ingredient import Ingredient

class Fruit(Ingredient):
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 sweetness=5, has_seeds=True, is_ripe=True):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not 0 <= sweetness <= 10:
            raise ValueError("Сладость должна быть от 0 до 10")
        self.__sweetness = sweetness
        self.__has_seeds = bool(has_seeds)
        self.__is_ripe = bool(is_ripe)
        self.__is_cut = False

    @property
    def sweetness(self): return self.__sweetness
    @property
    def has_seeds(self): return self.__has_seeds
    @property
    def is_ripe(self): return self.__is_ripe
    @property
    def is_cut(self): return self.__is_cut

    def ripen(self):
        self.__is_ripe = True
        return self.__is_ripe

    def cut(self):
        if not self.__is_ripe:
            raise ValueError("Неспелый фрукт нельзя подготовить для подачи")
        self.__is_cut = True
        return self.weight

    def calculate_sweetness_score(self):
        return self.__sweetness * self.weight / 100

    def remove_seeds(self):
        self.__has_seeds = False
        return True
