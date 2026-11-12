from culinary.exceptions import InvalidIngredientError
from .recipe_ingredient import RecipeIngredient
from .recipe_step import RecipeStep

class Recipe:
    """Рецепт с отдельными объектами ингредиентов и последовательностью шагов."""

    def __init__(self, name, description, preparation_minutes, servings):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название рецепта не может быть пустым")
        if preparation_minutes < 0 or servings <= 0:
            raise ValueError("Время не может быть отрицательным, количество порций должно быть положительным")
        self.__name = name.strip()
        self.__description = description
        self.__preparation_minutes = preparation_minutes
        self.__servings = servings
        self.__ingredients = []
        self.__steps = []

    @property
    def name(self): return self.__name
    @property
    def description(self): return self.__description
    @property
    def preparation_minutes(self): return self.__preparation_minutes
    @property
    def servings(self): return self.__servings
    @property
    def ingredients(self): return tuple(self.__ingredients)
    @property
    def steps(self): return tuple(self.__steps)

    def add_ingredient(self, ingredient, amount, unit="г", is_optional=False):
        if amount <= 0:
            raise InvalidIngredientError("Количество ингредиента должно быть положительным")
        item = RecipeIngredient(ingredient, amount, unit, is_optional)
        self.__ingredients.append(item)
        return item

    def remove_ingredient(self, ingredient):
        for item in self.__ingredients:
            if item.ingredient is ingredient:
                self.__ingredients.remove(item)
                return True
        return False

    def add_step(self, step):
        if not isinstance(step, RecipeStep):
            raise TypeError("Шаг рецепта должен быть объектом RecipeStep")
        if any(existing.number == step.number for existing in self.__steps):
            raise ValueError("Номер шага уже используется")
        self.__steps.append(step)
        self.__steps.sort(key=lambda item: item.number)

    def estimate_total_cost(self):
        return sum(item.calculate_cost() for item in self.__ingredients if not item.is_optional)

    def calculate_total_calories(self):
        return sum(item.ingredient.calculate_calories(item.amount) for item in self.__ingredients if not item.is_optional)

    def scale_servings(self, new_servings):
        if new_servings <= 0:
            raise ValueError("Количество порций должно быть положительным")
        factor = new_servings / self.__servings
        self.__ingredients = [RecipeIngredient(item.ingredient, item.amount * factor, item.unit, item.is_optional) for item in self.__ingredients]
        self.__servings = new_servings

    def format_steps(self):
        return [step.format_instruction() for step in self.__steps]
