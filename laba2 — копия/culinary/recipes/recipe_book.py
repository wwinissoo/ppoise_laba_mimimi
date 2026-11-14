from culinary.exceptions import InvalidRecipeException, RecipeNotFoundError
from culinary.validation import require_text
from .recipe import Recipe


class RecipeBook:
    """Кулинарная книга: именованная коллекция рецептов одного автора."""

    def __init__(self, title, author, recipes=None):
        self.__title = require_text(title, "Название книги не может быть пустым")
        self.__author = author
        self.__recipes = []
        for recipe in recipes or []:
            self.add_recipe(recipe)

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def recipes(self):
        return tuple(self.__recipes)

    def add_recipe(self, recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("В книгу можно добавить только Recipe")
        if self.find_by_name(recipe.name):
            raise InvalidRecipeException(f"Рецепт «{recipe.name}» уже есть в книге")
        self.__recipes.append(recipe)

    def find_by_name(self, name):
        key = name.strip().casefold()
        return [recipe for recipe in self.__recipes if recipe.name.casefold() == key]

    def get_by_name(self, name):
        """Возвращает рецепт по названию или сообщает о его отсутствии."""
        matches = self.find_by_name(name)
        if not matches:
            raise RecipeNotFoundError(f"Рецепт «{name}» не найден")
        return matches[0]

    def find_by_ingredient(self, ingredient_name):
        return [recipe for recipe in self.__recipes if recipe.has_ingredient(ingredient_name)]

    def count_recipes(self):
        return len(self.__recipes)
