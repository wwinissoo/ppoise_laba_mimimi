from culinary.exceptions import InvalidRecipeException, InvalidTemperatureException, PortionException
from culinary.recipes.recipe import Recipe
from culinary.validation import is_number, require_positive_int, require_text


class Dish:
    """Готовое блюдо, приготовленное по рецепту на заданное число порций."""

    MIN_SERVING_TEMPERATURE = -20
    MAX_SERVING_TEMPERATURE = 100

    def __init__(self, name, recipe, portions, serving_temperature):
        self.__name = require_text(name, "Название блюда не может быть пустым")
        if not isinstance(recipe, Recipe):
            raise TypeError("Блюдо должно ссылаться на объект Recipe")
        require_positive_int(portions, "Количество порций должно быть положительным целым числом", PortionException)
        self._validate_temperature(serving_temperature)
        self.__recipe = recipe
        self.__portions = portions
        self.__serving_temperature = serving_temperature

    @classmethod
    def _validate_temperature(cls, temperature):
        if not is_number(temperature) or not cls.MIN_SERVING_TEMPERATURE <= temperature <= cls.MAX_SERVING_TEMPERATURE:
            raise InvalidTemperatureException(
                f"Температура подачи должна быть от {cls.MIN_SERVING_TEMPERATURE} "
                f"до {cls.MAX_SERVING_TEMPERATURE} °C"
            )

    @property
    def name(self):
        return self.__name

    @property
    def recipe(self):
        return self.__recipe

    @property
    def portions(self):
        return self.__portions

    @property
    def serving_temperature(self):
        return self.__serving_temperature

    def prepare(self):
        return self.recipe.estimate_total_cost()

    def calculate_cost_per_portion(self):
        return self.recipe.estimate_total_cost() / self.portions

    def calculate_calories_per_portion(self):
        return self.recipe.calculate_total_calories() / self.portions

    def change_serving_temperature(self, temperature):
        self._validate_temperature(temperature)
        self.__serving_temperature = temperature

    def replace_recipe(self, recipe):
        """Подменяет технологическую карту обновлённой версией того же рецепта."""
        if not isinstance(recipe, Recipe):
            raise TypeError("Ожидается объект Recipe")
        if recipe.name.casefold() != self.__recipe.name.casefold():
            raise InvalidRecipeException("Новая версия рецепта должна иметь то же название")
        self.__recipe = recipe
