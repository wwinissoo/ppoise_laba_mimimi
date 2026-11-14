"""Расчёт калорийности ингредиентов, рецептов и блюд."""

from culinary.ingredients.ingredient import Ingredient
from culinary.recipes.recipe import Recipe
from culinary.validation import require_number


class CalorieCalculator:
    def calculate_ingredient(self, ingredient, amount_grams):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Ожидается объект Ingredient")
        return ingredient.calculate_calories(amount_grams)

    def calculate_recipe(self, recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Ожидается объект Recipe")
        return recipe.calculate_total_calories()

    def calculate_per_serving(self, recipe):
        return self.calculate_recipe(recipe) / recipe.servings

    def calculate_daily_balance(self, consumed_calories, target_calories):
        require_number(consumed_calories, "Потреблённые калории не могут быть отрицательными", minimum=0)
        require_number(target_calories, "Целевые калории должны быть положительными", positive=True)
        return target_calories - consumed_calories
