from culinary.dishes.dish import Dish
from culinary.exceptions import AllergenException
from culinary.validation import require_number, require_text


class DietPlan:
    """План питания: дневной лимит калорий, исключённые ингредиенты и приёмы пищи."""

    DEFAULT_CALORIE_LIMIT = 2000

    def __init__(self, title, excluded_ingredients=None, daily_calorie_limit=DEFAULT_CALORIE_LIMIT, meals=None):
        self.__title = require_text(title, "Название плана не может быть пустым")
        self.__excluded_ingredients = {
            require_text(name, "Исключаемый ингредиент не может быть пустым").casefold()
            for name in excluded_ingredients or []
        }
        self.__daily_calorie_limit = require_number(
            daily_calorie_limit, "Лимит калорий должен быть положительным", positive=True
        )
        self.__meals = []
        for meal in meals or []:
            self.add_meal(meal)

    @property
    def title(self):
        return self.__title

    @property
    def excluded_ingredients(self):
        return tuple(sorted(self.__excluded_ingredients))

    @property
    def daily_calorie_limit(self):
        return self.__daily_calorie_limit

    @property
    def meals(self):
        return tuple(self.__meals)

    def is_ingredient_allowed(self, ingredient):
        name = getattr(ingredient, "name", str(ingredient))
        return name.strip().casefold() not in self.__excluded_ingredients

    def is_dish_allowed(self, dish):
        return all(self.is_ingredient_allowed(item.ingredient) for item in dish.recipe.ingredients)

    def add_meal(self, dish):
        """Добавляет одну порцию блюда; блюда с запрещёнными ингредиентами отклоняются."""
        if not isinstance(dish, Dish):
            raise TypeError("Приём пищи должен быть объектом Dish")
        if not self.is_dish_allowed(dish):
            raise AllergenException(f"Блюдо «{dish.name}» содержит исключённый планом ингредиент")
        self.__meals.append(dish)

    def calculate_daily_calories(self):
        return sum(meal.calculate_calories_per_portion() for meal in self.__meals)

    def is_within_limit(self):
        return self.calculate_daily_calories() <= self.daily_calorie_limit

    def remaining_calories(self):
        return self.daily_calorie_limit - self.calculate_daily_calories()
