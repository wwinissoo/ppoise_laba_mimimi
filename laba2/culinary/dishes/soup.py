"""Суп."""

from culinary.ingredients.ingredient import Ingredient
from culinary.validation import require_text
from .dish import Dish


class Soup(Dish):
    """Суп на бульоне; к рецепту можно добавить дополнительные компоненты подачи."""

    DEFAULT_TEMPERATURE = 70
    MIN_HOT_TEMPERATURE = 60

    def __init__(self, name, recipe, portions, serving_temperature=DEFAULT_TEMPERATURE, broth="овощной"):
        super().__init__(name, recipe, portions, serving_temperature)
        self.__broth = require_text(broth, "Тип бульона не может быть пустым")
        self.__extra_components = []

    @property
    def broth(self):
        return self.__broth

    @property
    def extra_components(self):
        return tuple(self.__extra_components)

    def add_component(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Компонент супа должен быть объектом Ingredient")
        self.__extra_components.append(ingredient)

    def count_components(self):
        return len(self.recipe.ingredients) + len(self.__extra_components)

    def is_hot_enough(self, minimum=MIN_HOT_TEMPERATURE):
        return self.serving_temperature >= minimum
