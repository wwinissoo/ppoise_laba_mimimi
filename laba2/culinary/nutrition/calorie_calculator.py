"""Расчёт калорийности ингредиентов, рецептов и блюд."""
class CalorieCalculator:
    def calculate_ingredient(self,ingredient,amount_grams): return ingredient.calculate_calories(amount_grams)
    def calculate_recipe(self,recipe): return recipe.calculate_total_calories()
    def calculate_per_serving(self,recipe):
        if recipe.servings <= 0: raise ValueError("Количество порций должно быть положительным")
        return self.calculate_recipe(recipe)/recipe.servings
    def calculate_daily_balance(self,consumed_calories,target_calories): return target_calories-consumed_calories
