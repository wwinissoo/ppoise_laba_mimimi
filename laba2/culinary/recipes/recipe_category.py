class RecipeCategory:
    """Объект предметной области: RecipeCategory."""

    def __init__(self, name, description, recipes, dietary_tag):
        self.__name = name
        self.__description = description
        self.__recipes = recipes
        self.__dietary_tag = dietary_tag

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def recipes(self):
        return self.__recipes

    @property
    def dietary_tag(self):
        return self.__dietary_tag

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def remove_recipe(self, recipe):
        if recipe in self.recipes: self.recipes.remove(recipe)

    def matches_diet(self, tag):
        return self.dietary_tag == tag

