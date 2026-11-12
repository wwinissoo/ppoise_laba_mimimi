from culinary.exceptions import RecipeNotFoundError
class RecipeBook:
    """Объект предметной области: RecipeBook."""

    def __init__(self, title, author, recipes):
        self.__title = title
        self.__author = author
        self.__recipes = recipes

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def recipes(self):
        return self.__recipes

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def find_by_name(self, name):
        return [recipe for recipe in self.recipes if recipe.name.lower() == name.lower()]

    def get_by_name(self, name):
        """Возвращает рецепт по названию или сообщает о его отсутствии."""
        matches = self.find_by_name(name)
        if not matches:
            raise RecipeNotFoundError(f"Рецепт «{name}» не найден")
        return matches[0]

    def count_recipes(self):
        return len(self.recipes)

