import pytest

from culinary.dishes import Dish
from culinary.exceptions import AllergenException, PortionException
from culinary.ingredients import DairyProduct
from culinary.nutrition import (
    Allergen,
    CalorieCalculator,
    DietaryPlan,
    DietPlan,
    Nutrient,
    NutritionFacts,
    NutritionValue,
)
from culinary.recipes import Recipe


@pytest.fixture
def porridge():
    milk = DairyProduct("Молоко", 1000, 90, 60, 5, 4)
    recipe = Recipe("Каша", "", 15, 1)
    recipe.add_ingredient(milk, 200)
    return recipe


class TestAllergen:
    def test_detection(self, porridge):
        lactose = Allergen(" молоко ", "тяжёлая", "Непереносимость лактозы")
        assert lactose.name == "молоко" and lactose.severity == "тяжёлая"
        assert lactose.description == "Непереносимость лактозы"
        assert lactose.matches_ingredient("Молоко 3,2%") and lactose.find_in_recipe(porridge)
        assert lactose.describe() == "молоко: тяжёлая. Непереносимость лактозы"
        with pytest.raises(AllergenException):
            lactose.ensure_absent(porridge)
        assert Allergen("орехи").ensure_absent(porridge)

    def test_validation(self):
        with pytest.raises(ValueError):
            Allergen("орехи", "смертельная")
        with pytest.raises(ValueError):
            Allergen(" ")


class TestDietPlan:
    def test_calories(self, dish):
        plan = DietPlan("Лёгкий", ["Сахар"], 100, [dish])
        assert plan.title == "Лёгкий" and plan.excluded_ingredients == ("сахар",) and plan.meals == (dish,)
        assert plan.calculate_daily_calories() == pytest.approx(18)
        assert plan.is_within_limit() and plan.remaining_calories() == pytest.approx(82)
        assert plan.daily_calorie_limit == 100 and DietaryPlan is DietPlan

    def test_excluded_ingredients(self, dish):
        plan = DietPlan("Без томатов", ["помидор"])
        assert not plan.is_ingredient_allowed("Помидор") and not plan.is_dish_allowed(dish)
        with pytest.raises(AllergenException):
            plan.add_meal(dish)
        with pytest.raises(TypeError):
            plan.add_meal("салат")

    def test_validation(self):
        with pytest.raises(ValueError):
            DietPlan("План", daily_calorie_limit=0)
        with pytest.raises(ValueError):
            DietPlan("План", [" "])


class TestNutrient:
    def test_values(self):
        protein = Nutrient("Белок", 5, 60)
        assert protein.name == "Белок" and protein.unit == "г" and protein.amount_grams == 5
        assert protein.daily_value_grams == 60 and protein.daily_value_percentage() == pytest.approx(8.33, 0.01)
        assert protein.is_deficient() and not Nutrient("Белок", 30, 60).is_deficient()
        assert protein.convert_to_milligrams() == 5000
        assert Nutrient("Витамин C", 0.09, 0.09, "мг").amount_in_display_unit() == pytest.approx(90)
        assert NutritionValue is Nutrient

    def test_validation(self):
        with pytest.raises(ValueError):
            Nutrient("Белок", 10, 0)
        with pytest.raises(ValueError):
            Nutrient("Белок", 10, 50, "кг")


class TestNutritionFacts:
    def test_values(self):
        facts = NutritionFacts(250, 25, 10, 5, 100)
        assert (facts.calories, facts.protein, facts.fat, facts.carbohydrates, facts.serving_grams) == (
            250,
            25,
            10,
            5,
            100,
        )
        assert facts.calculate_energy_from_macros() == 210 and facts.is_high_protein()
        assert facts.scale_to_serving(200) == {"calories": 500, "protein": 50, "fat": 20, "carbohydrates": 10}

    def test_validation(self):
        with pytest.raises(ValueError):
            NutritionFacts(100, 60, 30, 20, 100)
        with pytest.raises(PortionException):
            NutritionFacts(100, 1, 1, 1, 0)
        with pytest.raises(PortionException):
            NutritionFacts(100, 1, 1, 1, 100).scale_to_serving(0)


class TestCalorieCalculator:
    def test_calculations(self, recipe, tomato):
        calculator = CalorieCalculator()
        assert calculator.calculate_ingredient(tomato, 100) == 18
        assert calculator.calculate_recipe(recipe) == pytest.approx(36)
        assert calculator.calculate_per_serving(recipe) == pytest.approx(18)
        assert calculator.calculate_daily_balance(1500, 2000) == 500
        assert Dish("Салат", recipe, 1, 10).calculate_calories_per_portion() == pytest.approx(36)

    def test_validation(self):
        calculator = CalorieCalculator()
        with pytest.raises(TypeError):
            calculator.calculate_recipe("рецепт")
        with pytest.raises(TypeError):
            calculator.calculate_ingredient("томат", 10)
        with pytest.raises(ValueError):
            calculator.calculate_daily_balance(-1, 2000)
