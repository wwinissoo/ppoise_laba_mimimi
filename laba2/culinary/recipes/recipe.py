from culinary.exceptions import CookingTimeException, InvalidRecipeStepError, PortionException
from culinary.validation import is_number, require_positive_int, require_text
from .recipe_ingredient import RecipeIngredient
from .recipe_step import RecipeStep


class Recipe:
    """Рецепт с отдельными объектами ингредиентов и последовательностью шагов."""

    def __init__(self, name, description, preparation_minutes, servings):
        self.__name = require_text(name, "Название рецепта не может быть пустым")
        if not is_number(preparation_minutes) or preparation_minutes < 0:
            raise CookingTimeException("Время приготовления не может быть отрицательным")
        self._validate_servings(servings)
        self.__description = str(description or "").strip()
        self.__preparation_minutes = preparation_minutes
        self.__servings = servings
        self.__ingredients = []
        self.__steps = []

    @staticmethod
    def _validate_servings(servings):
        require_positive_int(servings, "Количество порций должно быть положительным целым числом", PortionException)

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def preparation_minutes(self):
        return self.__preparation_minutes

    @property
    def servings(self):
        return self.__servings

    @property
    def ingredients(self):
        return tuple(self.__ingredients)

    @property
    def steps(self):
        return tuple(self.__steps)

    def add_ingredient(self, ingredient, amount, unit="г", is_optional=False):
        item = RecipeIngredient(ingredient, amount, unit, is_optional)
        self.__ingredients.append(item)
        return item

    def remove_ingredient(self, ingredient):
        for item in self.__ingredients:
            if item.ingredient is ingredient:
                self.__ingredients.remove(item)
                return True
        return False

    def has_ingredient(self, ingredient_name):
        name = ingredient_name.strip().casefold()
        return any(item.ingredient.name.casefold() == name for item in self.__ingredients)

    def add_step(self, step):
        if not isinstance(step, RecipeStep):
            raise TypeError("Шаг рецепта должен быть объектом RecipeStep")
        if any(existing.number == step.number for existing in self.__steps):
            raise InvalidRecipeStepError("Номер шага уже используется")
        self.__steps.append(step)
        self.__steps.sort(key=lambda item: item.number)

    def calculate_requirements(self, multiplier=1):
        """Обязательные ингредиенты с суммарным количеством: [(ингредиент, граммы, кг)]."""
        totals = {}
        for item in self.__ingredients:
            if not item.is_optional:
                ingredient, grams, kilograms = totals.get(id(item.ingredient), (item.ingredient, 0, 0))
                grams += item.amount_in_grams(multiplier)
                kilograms += item.amount_in_kilograms(multiplier)
                totals[id(ingredient)] = (ingredient, grams, kilograms)
        return list(totals.values())

    def calculate_steps_duration(self):
        return sum(step.duration_minutes for step in self.__steps)

    def estimate_total_cost(self):
        return sum(item.calculate_cost() for item in self.__ingredients if not item.is_optional)

    def calculate_total_calories(self):
        return sum(item.calculate_calories() for item in self.__ingredients if not item.is_optional)

    def scale_servings(self, new_servings):
        self._validate_servings(new_servings)
        factor = new_servings / self.__servings
        self.__ingredients = [
            RecipeIngredient(item.ingredient, item.amount * factor, item.unit, item.is_optional)
            for item in self.__ingredients
        ]
        self.__servings = new_servings

    def format_steps(self):
        return [step.format_instruction() for step in self.__steps]
