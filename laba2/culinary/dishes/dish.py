class Dish:
    """Объект предметной области: Dish."""

    def __init__(self, name, recipe, portions, serving_temperature):
        self.__name = name
        self.__recipe = recipe
        self.__portions = portions
        self.__serving_temperature = serving_temperature

    @property
    def name(self):
        return self.__name

    @property
    def recipe(self):
        return self.__recipe

    @property
    def portions(self):
        return self.__portions

    @property
    def serving_temperature(self):
        return self.__serving_temperature

    def prepare(self):
        return self.recipe.estimate_total_cost()

    def calculate_cost_per_portion(self):
        if self.portions <= 0: raise ValueError('Порции должны быть положительными')
        return self.recipe.estimate_total_cost() / self.portions

    def change_serving_temperature(self, temperature):
        self.__serving_temperature = temperature

