"""Управление коллекцией рецептов."""
from culinary.exceptions import RecipeNotFoundError
class RecipeManager:
    """Добавляет, ищет и удаляет рецепты по названию."""
    def __init__(self): self.__recipes = {}
    @property
    def recipes(self): return tuple(self.__recipes.values())
    def add_recipe(self, recipe):
        if not hasattr(recipe, "name"): raise TypeError("Ожидается объект рецепта")
        self.__recipes[recipe.name.casefold()] = recipe
    def find_recipe(self, name):
        recipe = self.__recipes.get(name.casefold())
        if recipe is None: raise RecipeNotFoundError(f"Рецепт «{name}» не найден")
        return recipe
    def remove_recipe(self, name):
        return self.__recipes.pop(name.casefold(), None) is not None
    def search_by_ingredient(self, ingredient_name):
        result=[]
        for recipe in self.__recipes.values():
            if any(getattr(item.ingredient, "name", "").casefold()==ingredient_name.casefold() for item in recipe.ingredients): result.append(recipe)
        return result
