class DietPlan:
    """Объект предметной области: DietPlan."""

    def __init__(self, title, excluded_ingredients, daily_calorie_limit, meals):
        self.__title = title
        self.__excluded_ingredients = excluded_ingredients
        self.__daily_calorie_limit = daily_calorie_limit
        self.__meals = meals

    @property
    def title(self):
        return self.__title

    @property
    def excluded_ingredients(self):
        return self.__excluded_ingredients

    @property
    def daily_calorie_limit(self):
        return self.__daily_calorie_limit

    @property
    def meals(self):
        return self.__meals

    def add_meal(self, dish):
        self.meals.append(dish)

    def is_ingredient_allowed(self, ingredient):
        return ingredient.name not in self.excluded_ingredients

    def calculate_daily_calories(self):
        total_calories = 0
        for meal in self.meals:
            recipe = getattr(meal, 'recipe', None)
            if recipe is None:
                total_calories += getattr(meal, 'calories', 0)
                continue
            for ingredient, amount in recipe.ingredients:
                total_calories += ingredient.calculate_calories(amount)
        return total_calories

