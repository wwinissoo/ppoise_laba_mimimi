class Garnish:
    """Объект предметной области: Garnish."""

    def __init__(self, name, ingredients, weight, decoration_style):
        self.__name = name
        self.__ingredients = ingredients
        self.__weight = weight
        self.__decoration_style = decoration_style

    @property
    def name(self):
        return self.__name

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def weight(self):
        return self.__weight

    @property
    def decoration_style(self):
        return self.__decoration_style

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def calculate_ingredient_weight(self):
        return sum(item.weight for item in self.ingredients)

    def is_light_garnish(self, limit=150):
        return self.weight <= limit

