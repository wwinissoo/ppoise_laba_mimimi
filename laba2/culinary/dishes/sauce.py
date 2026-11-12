class Sauce:
    """Объект предметной области: Sauce."""

    def __init__(self, name, base_ingredient, consistency, volume):
        self.__name = name
        self.__base_ingredient = base_ingredient
        self.__consistency = consistency
        self.__volume = volume

    @property
    def name(self):
        return self.__name

    @property
    def base_ingredient(self):
        return self.__base_ingredient

    @property
    def consistency(self):
        return self.__consistency

    @property
    def volume(self):
        return self.__volume

    def thicken(self, amount):
        if amount <= 0: raise ValueError('Количество должно быть положительным')
        self.__volume += amount
        self.__consistency = 'густой'

    def dilute(self, amount):
        if amount <= 0 or amount >= self.volume: raise ValueError('Некорректный объём')
        self.__volume -= amount
        self.__consistency = 'жидкий'

    def is_based_on(self, ingredient):
        return self.base_ingredient is ingredient

