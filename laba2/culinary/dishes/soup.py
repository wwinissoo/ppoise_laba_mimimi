class Soup:
    """Объект предметной области: Soup."""

    def __init__(self, name, broth, ingredients, serving_temperature):
        self.__name = name
        self.__broth = broth
        self.__ingredients = ingredients
        self.__serving_temperature = serving_temperature

    @property
    def name(self):
        return self.__name

    @property
    def broth(self):
        return self.__broth

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def serving_temperature(self):
        return self.__serving_temperature

    def add_component(self, ingredient):
        self.ingredients.append(ingredient)

    def count_components(self):
        return len(self.ingredients)

    def is_hot_enough(self, minimum=60):
        return self.serving_temperature >= minimum

