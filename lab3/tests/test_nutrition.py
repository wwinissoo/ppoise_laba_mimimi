import pytest

from fitness.exceptions import EntityNotFoundError, InvalidValueError, NutritionLimitError
from fitness.nutrition import CalorieCalculator, Food, FoodPortion, MacroTargets, Meal, NutritionDiary, Supplement
from fitness.users import BodyMeasurement, User
from tests.conftest import NOW, TODAY


@pytest.fixture
def chicken():
    return Food("Курица", 165, 31, 3.6, 0)


@pytest.fixture
def rice():
    return Food("Рис", 130, 2.7, 0.3, 28)


@pytest.fixture
def lunch(chicken, rice):
    meal = Meal("обед", NOW)
    meal.add_portion(FoodPortion(chicken, 200))
    meal.add_portion(FoodPortion(rice, 100))
    return meal


class TestFood:
    def test_food(self, chicken):
        assert chicken.nutrients_for(200) == {"калории": 330, "белки": 62, "жиры": 7.2, "углеводы": 0}
        assert chicken.is_high_protein() and chicken.grams_for_calories(330) == 200
        assert (chicken.name, chicken.calories_per_100g, chicken.protein_g, chicken.fat_g, chicken.carbs_g) == (
            "Курица",
            165,
            31,
            3.6,
            0,
        )
        water = Food("Вода", 0, 0, 0, 0)
        assert not water.is_high_protein()
        with pytest.raises(InvalidValueError):
            water.grams_for_calories(10)
        with pytest.raises(InvalidValueError):
            Food("X", 100, 60, 30, 20)

    def test_portion_and_meal(self, lunch, chicken):
        portion = FoodPortion(chicken, 100)
        assert portion.calories() == 165 and portion.scaled(2).grams == 200 and portion.food is chicken
        assert lunch.total_calories() == 460 and lunch.macros() == {"белки": 64.7, "жиры": 7.5, "углеводы": 28}
        assert lunch.dominant_macro() == "белки" and lunch.meal_type == "обед" and lunch.eaten_at == NOW
        assert lunch.remove_food("РИС").grams == 100 and len(lunch.portions) == 1
        with pytest.raises(EntityNotFoundError):
            lunch.remove_food("рис")
        assert Meal("ужин", NOW).dominant_macro() is None
        with pytest.raises(InvalidValueError):
            Meal("полдник", NOW)


class TestMacroTargets:
    def test_targets(self):
        targets = MacroTargets.from_calories(2000)
        assert targets.as_dict() == {"белки": 150, "жиры": 56, "углеводы": 225} and targets.calories() == 2004
        assert targets.deviation({"белки": 140}) == {"белки": -10, "жиры": -56, "углеводы": -225}
        assert targets.is_balanced({"белки": 150, "жиры": 56, "углеводы": 225})
        assert not targets.is_balanced({"белки": 100, "жиры": 56, "углеводы": 225})
        assert (targets.protein_g, targets.fat_g, targets.carbs_g) == (150, 56, 225)
        with pytest.raises(InvalidValueError):
            MacroTargets.from_calories(2000, 0.6, 0.5)


class TestNutritionDiary:
    def test_diary(self, user, lunch, measurement):
        diary = NutritionDiary(user, TODAY, 2000)
        diary.add_meal(lunch)
        assert diary.total_calories() == 460 and diary.remaining_calories() == 1540 and not diary.is_over_target()
        assert diary.total_macros() == lunch.macros() and diary.drink_water(500) == 500 and diary.water_ml == 500
        assert diary.macro_report(MacroTargets(60, 10, 30)) == {"белки": 4.7, "жиры": -2.5, "углеводы": -2}
        assert diary.user is user and diary.day == TODAY and diary.calorie_target == 2000 and diary.meals == (lunch,)
        with pytest.raises(InvalidValueError):
            diary.water_goal_ml()
        user.add_measurement(measurement)
        assert diary.water_goal_ml() == 1800
        feast = Meal("ужин", NOW)
        feast.add_portion(FoodPortion(Food("Масло", 900, 0, 100, 0), 300))
        diary.add_meal(feast)
        assert diary.is_over_target()
        with pytest.raises(InvalidValueError):
            diary.add_meal(Meal("завтрак", NOW.replace(day=1)))


class TestCalorieCalculator:
    def test_calculations(self, user, measurement, policy):
        calculator = CalorieCalculator()
        with pytest.raises(InvalidValueError):
            calculator.basal_metabolic_rate(user, TODAY)
        user.add_measurement(measurement)
        assert calculator.basal_metabolic_rate(user, TODAY) == 1372 and calculator.basal_metabolic_rate(user) > 0
        assert calculator.daily_energy_expenditure(user, TODAY) == 2127
        assert calculator.calorie_target(user, "похудение", TODAY) == 1627
        assert calculator.calorie_target(user, "набор массы", TODAY, measurement) == 2427
        calculator.change_activity_level("минимальная")
        assert (
            calculator.activity_level == "минимальная" and calculator.calorie_target(user, "похудение", TODAY) == 1200
        )
        male = User.register("oleg", "o@o.ru", "Secret123", TODAY.replace(year=1990), User.MALE, policy)
        assert calculator.basal_metabolic_rate(male, TODAY, BodyMeasurement(TODAY, 80, 180)) == 1750
        with pytest.raises(InvalidValueError):
            calculator.calorie_target(user, "сушка", TODAY)


class TestSupplement:
    def test_doses(self):
        creatine = Supplement("Креатин", 5000, 10000)
        assert creatine.take() == 5000 and creatine.remaining_mg() == 5000 and creatine.doses_left() == 1
        with pytest.raises(NutritionLimitError):
            creatine.take(2)
        creatine.reset_day()
        assert creatine.taken_today_mg == 0 and creatine.name == "Креатин"
        assert creatine.dose_mg == 5000 and creatine.max_daily_mg == 10000
        with pytest.raises(NutritionLimitError):
            Supplement("X", 10, 5)
