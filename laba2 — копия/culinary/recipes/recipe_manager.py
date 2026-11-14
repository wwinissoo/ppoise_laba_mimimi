"""Управление коллекцией рецептов."""

from culinary.exceptions import RecipeNotFoundError
from culinary.exceptions import InvalidRecipeException
from .recipe import Recipe


class RecipeManager:
    """Добавляет, ищет и удаляет рецепты по названию."""

    def __init__(self):
        self.__recipes = {}

    @property
    def recipes(self):
        return tuple(self.__recipes.values())

    @staticmethod
    def _key(name):
        if not isinstance(name, str):
            raise TypeError("Название рецепта должно быть строкой")
        return name.strip().casefold()

    @staticmethod
    def _require_recipe(recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Ожидается объект Recipe")

    def add_recipe(self, recipe):
        self._require_recipe(recipe)
        key = self._key(recipe.name)
        if key in self.__recipes:
            raise InvalidRecipeException(f"Рецепт «{recipe.name}» уже существует")
        self.__recipes[key] = recipe

    def update_recipe(self, name, recipe):
        self._require_recipe(recipe)
        key = self._key(name)
        if key not in self.__recipes:
            raise RecipeNotFoundError(f"Рецепт «{name}» не найден")
        if self._key(recipe.name) != key:
            raise InvalidRecipeException("Имя обновляемого рецепта должно совпадать")
        self.__recipes[key] = recipe
        return recipe

    def find_recipe(self, name):
        recipe = self.__recipes.get(self._key(name))
        if recipe is None:
            raise RecipeNotFoundError(f"Рецепт «{name}» не найден")
        return recipe

    def remove_recipe(self, name):
        return self.__recipes.pop(self._key(name), None) is not None

    def search_by_ingredient(self, ingredient_name):
        return [recipe for recipe in self.__recipes.values() if recipe.has_ingredient(ingredient_name)]
