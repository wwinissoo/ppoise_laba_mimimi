from culinary.validation import require_text
from .recipe import Recipe


class RecipeCategory:
    """Категория рецептов (первые блюда, десерты…) с диетической меткой."""

    def __init__(self, name, description, recipes=None, dietary_tag=None):
        self.__name = require_text(name, "Название категории не может быть пустым")
        self.__description = str(description or "").strip()
        self.__recipes = []
        self.__dietary_tag = dietary_tag
        for recipe in recipes or []:
            self.add_recipe(recipe)

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def recipes(self):
        return tuple(self.__recipes)

    @property
    def dietary_tag(self):
        return self.__dietary_tag

    def add_recipe(self, recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("В категорию можно добавить только Recipe")
        if recipe not in self.__recipes:
            self.__recipes.append(recipe)

    def remove_recipe(self, recipe):
        if recipe in self.__recipes:
            self.__recipes.remove(recipe)
            return True
        return False

    def matches_diet(self, tag):
        return self.dietary_tag is not None and self.dietary_tag.casefold() == str(tag).casefold()
