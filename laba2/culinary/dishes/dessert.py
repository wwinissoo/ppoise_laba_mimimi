class Dessert:
    """Объект предметной области: Dessert."""

    def __init__(self, name, ingredients, sugar_grams, chilled):
        self.__name = name
        self.__ingredients = ingredients
        self.__sugar_grams = sugar_grams
        self.__chilled = chilled

    @property
    def name(self):
        return self.__name

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def sugar_grams(self):
        return self.__sugar_grams

    @property
    def chilled(self):
        return self.__chilled

    def add_component(self, ingredient):
        self.ingredients.append(ingredient)

    def is_low_sugar(self, limit=10):
        return self.sugar_grams <= limit

    def chill(self):
        self.__chilled = True

