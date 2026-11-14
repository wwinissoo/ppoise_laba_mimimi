import pytest

from culinary.exceptions import (
    CookingTimeException,
    InvalidIngredientError,
    InvalidRecipeException,
    InvalidRecipeStepError,
    InvalidTemperatureException,
    PortionException,
    RecipeNotFoundError,
)
from culinary.ingredients import Vegetable
from culinary.recipes import (
    CookingInstruction,
    CookingTime,
    Recipe,
    RecipeBook,
    RecipeCategory,
    RecipeIngredient,
    RecipeManager,
    RecipeStep,
    Serving,
)


class TestRecipeIngredient:
    def test_unit_conversion(self, tomato):
        entry = RecipeIngredient(tomato, 0.5, " кг ", False)
        assert entry.unit == "кг" and entry.amount_in_grams() == 500 and entry.amount_in_kilograms(2) == 1
        assert entry.calculate_cost() == pytest.approx(100) and entry.calculate_calories() == pytest.approx(90)
        assert entry.describe_amount() == "0.5 кг Помидор"

    @pytest.mark.parametrize("amount, unit", [(0, "г"), (True, "г"), (10, " "), (10, "шт")])
    def test_invalid(self, tomato, amount, unit):
        with pytest.raises(InvalidIngredientError):
            RecipeIngredient(tomato, amount, unit, False)

    def test_requires_ingredient(self):
        with pytest.raises(TypeError):
            RecipeIngredient("помидор", 10, "г", False)

    def test_consume_from_stock(self, tomato):
        RecipeIngredient(tomato, 100, "г", True).consume_from_stock()
        assert tomato.weight == 900


class TestRecipe:
    def test_units_are_respected(self, tomato):
        recipe = Recipe("Томаты", "", 5, 1)
        recipe.add_ingredient(tomato, 0.5, "кг")
        assert recipe.estimate_total_cost() == pytest.approx(100)
        assert recipe.calculate_total_calories() == pytest.approx(90)

    def test_validation(self, tomato):
        with pytest.raises(ValueError):
            Recipe(" ", "", 1, 1)
        with pytest.raises(CookingTimeException):
            Recipe("X", "", -1, 1)
        with pytest.raises(PortionException):
            Recipe("X", "", 1, 0)
        with pytest.raises(TypeError):
            Recipe("X", "", 1, 1).add_ingredient("помидор", 100)

    def test_ingredients_management(self, recipe, tomato):
        optional = Vegetable("Укроп", 100, 500, 40, 5, 4)
        recipe.add_ingredient(optional, 10, is_optional=True)
        recipe.add_ingredient(tomato, 100)
        assert recipe.has_ingredient(" укроп ") and not recipe.has_ingredient("лук")
        assert recipe.calculate_requirements(2) == [(tomato, 600, pytest.approx(0.6))]
        assert recipe.estimate_total_cost() == pytest.approx(60)
        assert recipe.remove_ingredient(optional) and not recipe.remove_ingredient(optional)
        assert recipe.description == "Овощной салат"

    def test_steps_and_scaling(self, recipe):
        recipe.add_step(RecipeStep(2, "Заправить", 2, None))
        recipe.add_step(RecipeStep(1, "Нарезать", 5, None))
        assert recipe.format_steps() == ["1. Нарезать", "2. Заправить"] and len(recipe.steps) == 2
        assert recipe.calculate_steps_duration() == 7
        with pytest.raises(InvalidRecipeStepError):
            recipe.add_step(RecipeStep(1, "Дубль", 1, None))
        with pytest.raises(TypeError):
            recipe.add_step("шаг")
        recipe.scale_servings(4)
        assert recipe.ingredients[0].amount == 400 and recipe.servings == 4
        with pytest.raises(PortionException):
            recipe.scale_servings(0)


class TestRecipeStep:
    def test_formatting(self):
        step = RecipeStep(3, " Обжарить ", 7, 180)
        assert step.format_instruction() == "3. Обжарить" and step.temperature == 180
        assert step.calculate_end_minute(10) == 17
        with pytest.raises(InvalidRecipeStepError):
            step.calculate_end_minute(-1)

    @pytest.mark.parametrize("number, text, minutes", [(0, "a", 1), (True, "a", 1), (1, " ", 1), (1, "a", -1)])
    def test_invalid(self, number, text, minutes):
        with pytest.raises(InvalidRecipeStepError):
            RecipeStep(number, text, minutes, None)

    def test_temperature(self):
        with pytest.raises(InvalidTemperatureException):
            RecipeStep(1, "Жарить", 5, 500)
        with pytest.raises(InvalidTemperatureException):
            RecipeStep(1, "Жарить", 5, "горячо")


class TestRecipeManager:
    def test_crud(self, recipe):
        manager = RecipeManager()
        manager.add_recipe(recipe)
        with pytest.raises(InvalidRecipeException):
            manager.add_recipe(recipe)
        assert manager.find_recipe("  салат ") is recipe and manager.recipes == (recipe,)
        assert manager.search_by_ingredient("помидор") == [recipe]
        new_version = Recipe("САЛАТ", "", 1, 1)
        assert manager.update_recipe("салат", new_version) is new_version
        assert manager.remove_recipe("Салат") and not manager.remove_recipe("Салат")
        with pytest.raises(RecipeNotFoundError):
            manager.find_recipe("Салат")

    def test_errors(self, recipe):
        manager = RecipeManager()
        with pytest.raises(TypeError):
            manager.add_recipe("рецепт")
        with pytest.raises(TypeError):
            manager.find_recipe(42)
        with pytest.raises(RecipeNotFoundError):
            manager.update_recipe("Салат", recipe)
        manager.add_recipe(recipe)
        with pytest.raises(InvalidRecipeException):
            manager.update_recipe("Салат", Recipe("Суп", "", 1, 1))


class TestRecipeBook:
    def test_collection(self, recipe):
        book = RecipeBook("Книга", "Автор", [recipe])
        assert book.title == "Книга" and book.author == "Автор" and book.count_recipes() == 1
        with pytest.raises(AttributeError):
            book.recipes.append(recipe)
        assert book.get_by_name("салат") is recipe and book.find_by_ingredient("Помидор") == [recipe]
        with pytest.raises(RecipeNotFoundError):
            book.get_by_name("Суп")

    def test_rules(self, recipe):
        book = RecipeBook("Книга", "Автор")
        book.add_recipe(recipe)
        with pytest.raises(InvalidRecipeException):
            book.add_recipe(recipe)
        with pytest.raises(TypeError):
            book.add_recipe("рецепт")


class TestRecipeCategory:
    def test_collection(self, recipe):
        category = RecipeCategory("Салаты", "Холодные", [recipe, recipe], "веган")
        assert category.name == "Салаты" and category.description == "Холодные" and len(category.recipes) == 1
        assert category.dietary_tag == "веган" and category.matches_diet("ВЕГАН")
        assert category.remove_recipe(recipe) and not category.remove_recipe(recipe)
        assert not RecipeCategory("Супы", None).matches_diet("веган")
        with pytest.raises(TypeError):
            category.add_recipe("рецепт")


class TestCookingTime:
    def test_minutes_and_hours(self):
        assert CookingTime(10, 15, 5).is_quick_recipe()
        time = CookingTime(0.5, 1, 0, "ч")
        assert time.total_minutes() == 90 and not time.is_quick_recipe()
        time.add_resting_time(30)
        assert time.resting == 0.5 and time.preparation == 0.5 and time.cooking == 1 and time.unit == "ч"

    def test_validation(self):
        with pytest.raises(CookingTimeException):
            CookingTime(-1, 0, 0)
        with pytest.raises(CookingTimeException):
            CookingTime(1, 0, 0, "сут")
        with pytest.raises(CookingTimeException):
            CookingTime(1, 0, 0).add_resting_time(-5)


class TestCookingInstruction:
    def test_behaviour(self):
        instruction = CookingInstruction("Нарезка", "Нарезать кубиками", "лёгкая", "Острый нож")
        assert instruction.title == "Нарезка" and instruction.difficulty == "лёгкая"
        assert instruction.validate_text() and instruction.has_safety_warning()
        assert instruction.safety_note == "Острый нож"
        assert instruction.shorten(7) == "Нарезат…" and instruction.shorten(100) == instruction.text
        assert not CookingInstruction("A", "B", "сложная", None).has_safety_warning()

    def test_validation(self):
        with pytest.raises(ValueError):
            CookingInstruction("A", "B", "экстрим")
        with pytest.raises(ValueError):
            CookingInstruction("A", "B", "лёгкая").shorten(0)


class TestServing:
    def test_behaviour(self):
        serving = Serving(60, " тарелка ", 250)
        assert serving.describe() == "Подача: тарелка; 250 г; 60 °C"
        assert serving.calculate_total_weight(2) == 500 and serving.presentation == "тарелка"
        assert serving.temperature_celsius == 60 and serving.serving_size_grams == 250

    def test_validation(self):
        with pytest.raises(InvalidTemperatureException):
            Serving(200, "тарелка", 250)
        with pytest.raises(PortionException):
            Serving(60, "тарелка", 0)
        with pytest.raises(PortionException):
            Serving(60, "тарелка", 250).calculate_total_weight(0)
