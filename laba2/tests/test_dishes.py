from datetime import date

import pytest

from culinary.dishes import (
    Beverage,
    Dessert,
    Dish,
    Garnish,
    MainCourse,
    Menu,
    MenuItem,
    Pastry,
    Portion,
    Salad,
    Sauce,
    Soup,
)
from culinary.exceptions import (
    CookingTimeException,
    DishUnavailableError,
    InvalidRecipeException,
    InvalidTemperatureException,
    PortionException,
)
from culinary.kitchen import Oven
from culinary.recipes import Recipe


class TestDish:
    def test_validation(self, recipe):
        with pytest.raises(ValueError):
            Dish(" ", recipe, 2, 12)
        with pytest.raises(TypeError):
            Dish("Салат", None, 2, 12)
        with pytest.raises(PortionException):
            Dish("Салат", recipe, 0, 12)
        with pytest.raises(InvalidTemperatureException):
            Dish("Салат", recipe, 2, 500)

    def test_cost_and_calories(self, dish):
        assert dish.prepare() == pytest.approx(40)
        assert dish.calculate_cost_per_portion() == pytest.approx(20)
        assert dish.calculate_calories_per_portion() == pytest.approx(18)

    def test_serving_temperature(self, dish):
        dish.change_serving_temperature(5)
        assert dish.serving_temperature == 5
        with pytest.raises(InvalidTemperatureException):
            dish.change_serving_temperature(200)

    def test_replace_recipe(self, dish):
        new_version = Recipe("салат", "", 1, 1)
        dish.replace_recipe(new_version)
        assert dish.recipe is new_version
        with pytest.raises(InvalidRecipeException):
            dish.replace_recipe(Recipe("Суп", "", 1, 1))
        with pytest.raises(TypeError):
            dish.replace_recipe("рецепт")


class TestSoup:
    def test_components(self, recipe, tomato):
        soup = Soup("Суп", recipe, 2, broth="куриный")
        soup.add_component(tomato)
        assert soup.count_components() == 2 and soup.extra_components == (tomato,)
        assert soup.broth == "куриный" and soup.is_hot_enough() and isinstance(soup, Dish)
        with pytest.raises(TypeError):
            soup.add_component("лук")


class TestDessert:
    def test_sugar_and_chilling(self, recipe):
        dessert = Dessert("Десерт", recipe, 2, sugar_grams=30, chilled=True)
        assert dessert.chilled and dessert.serving_temperature == Dessert.CHILLED_TEMPERATURE
        assert dessert.sugar_grams == 30 and dessert.calculate_sugar_per_portion() == 15
        assert not dessert.is_low_sugar() and Dessert("Желе", recipe, 2, sugar_grams=10).is_low_sugar()
        with pytest.raises(ValueError):
            Dessert("Десерт", recipe, 2, sugar_grams=-1)


class TestBeverage:
    def test_volume(self, recipe):
        juice = Beverage("Сок", recipe, 2, 8, 500, is_carbonated=True)
        assert juice.is_carbonated and juice.serving_volume() == 250
        assert juice.dilute(100) == 600 and juice.volume_ml == 600
        with pytest.raises(ValueError):
            juice.dilute(0)
        with pytest.raises(ValueError):
            Beverage("Сок", recipe, 2, 8, 0)


class TestPastry:
    def test_baking(self, recipe):
        pie = Pastry("Пирог", recipe, 2, 40, 220, 30)
        assert pie.baking_temperature == 220 and pie.baking_minutes == 30
        assert pie.estimate_baking_end(10) == 40
        assert pie.can_bake_in(Oven("Духовка", 2000, "выключено", 0, 250))
        assert not pie.can_bake_in(Oven("Мини", 800, "выключено", 0, 200))
        with pytest.raises(TypeError):
            pie.can_bake_in("печь")
        with pytest.raises(CookingTimeException):
            pie.estimate_baking_end(-1)

    def test_validation(self, recipe):
        with pytest.raises(InvalidTemperatureException):
            Pastry("Пирог", recipe, 2, 40, 400, 30)
        with pytest.raises(CookingTimeException):
            Pastry("Пирог", recipe, 2, 40, 200, 0)


class TestGarnish:
    def test_composition(self, tomato):
        garnish = Garnish("Овощи гриль", [(tomato, 100)], 150, "башенка")
        assert garnish.name == "Овощи гриль" and garnish.decoration_style == "башенка"
        assert garnish.ingredients == ((tomato, 100),) and garnish.calculate_ingredient_weight() == 100
        assert garnish.is_light_garnish() and not Garnish("Пюре", weight=300).is_light_garnish()
        assert garnish.weight == 150

    def test_rules(self, tomato):
        garnish = Garnish("Овощи", [(tomato, 100)], 150)
        with pytest.raises(PortionException):
            garnish.add_ingredient(tomato, 100)
        with pytest.raises(PortionException):
            garnish.add_ingredient(tomato, 0)
        with pytest.raises(TypeError):
            garnish.add_ingredient("лук", 10)


class TestMainCourse:
    def test_side_dish(self, recipe):
        course = MainCourse("Стейк", recipe, 1, 65)
        assert not course.has_side_dish() and course.side_dish is None
        garnish = Garnish("Картофель")
        course.attach_side_dish(garnish)
        assert course.has_side_dish() and course.side_dish is garnish
        assert MainCourse("Котлета", recipe, 1, 65, side_dish=garnish).has_side_dish()
        with pytest.raises(TypeError):
            course.attach_side_dish("картошка")


class TestSauce:
    def test_consistency(self, tomato):
        sauce = Sauce("Томатный", tomato)
        assert sauce.name == "Томатный" and sauce.is_based_on(tomato)
        sauce.dilute(20)
        assert sauce.volume == 120 and sauce.consistency == "жидкий"
        sauce.reduce(50)
        assert sauce.volume == 70 and sauce.consistency == "густой"
        sauce.thicken(10)
        assert sauce.volume == 80 and sauce.base_ingredient is tomato

    def test_rules(self, tomato):
        with pytest.raises(TypeError):
            Sauce("Соус", "томат")
        with pytest.raises(ValueError):
            Sauce("Соус", tomato, "твёрдый")
        with pytest.raises(ValueError):
            Sauce("Соус", tomato, volume=50).reduce(50)


class TestSalad:
    def test_dressing(self, recipe, tomato):
        sauce = Sauce("Томатный", tomato)
        salad = Salad("Салат", recipe, 2, dressing=sauce)
        assert salad.dressing is sauce and salad.is_served_chilled()
        assert Salad("Тёплый", recipe, 2, 40).dressing is None
        with pytest.raises(TypeError):
            salad.add_dressing("майонез")


class TestPortion:
    def test_behaviour(self, dish):
        portion = Portion(dish, 250, 150, 3)
        assert portion.dish is dish and portion.price == 150 and portion.table_number == 3
        assert portion.calculate_price_per_gram() == pytest.approx(0.6) and portion.is_for_table(3)
        portion.increase_weight(50)
        assert portion.weight == 300

    @pytest.mark.parametrize("weight, price, table", [(0, 1, 1), (1, -1, 1), (1, 1, 0), (1, 1, True)])
    def test_validation(self, dish, weight, price, table):
        with pytest.raises(PortionException):
            Portion(dish, weight, price, table)

    def test_requires_dish(self):
        with pytest.raises(TypeError):
            Portion("салат", 1, 1, 1)


class TestMenu:
    def test_dishes(self, dish):
        menu = Menu("Летнее", [dish], date(2026, 6, 1), date(2026, 8, 31))
        assert menu.title == "Летнее" and menu.valid_from == date(2026, 6, 1) and menu.valid_to == date(2026, 8, 31)
        assert menu.find_dish(" САЛАТ ") is dish and menu.find_dishes_under_price(25) == [dish]
        assert menu.find_dishes_under_price(10) == []
        assert menu.remove_dish(dish) and not menu.remove_dish(dish) and menu.dishes == ()

    def test_period(self):
        menu = Menu("Летнее", valid_from=date(2026, 6, 1), valid_to=date(2026, 8, 31))
        assert menu.is_active(date(2026, 7, 1)) and not menu.is_active(date(2026, 9, 1))
        assert Menu("Постоянное").is_active()
        with pytest.raises(ValueError):
            Menu("Неверное", valid_from=date(2026, 9, 1), valid_to=date(2026, 8, 1))

    def test_rules(self, dish):
        menu = Menu("Летнее", [dish])
        with pytest.raises(DishUnavailableError):
            menu.add_dish(dish)
        with pytest.raises(TypeError):
            menu.add_dish("салат")


class TestMenuItem:
    def test_pricing(self, dish):
        item = MenuItem(dish, 100)
        assert item.category == "основное" and item.available
        assert item.apply_discount(10) == 90 and item.price == 90
        assert item.calculate_margin() == pytest.approx(70)
        with pytest.raises(ValueError):
            item.apply_discount(150)

    def test_availability(self, dish):
        item = MenuItem(dish, 100, False, "салаты")
        with pytest.raises(DishUnavailableError):
            item.require_available()
        item.mark_available()
        assert item.require_available()
        item.mark_unavailable()
        assert not item.available

    def test_validation(self, dish):
        with pytest.raises(ValueError):
            MenuItem(dish, -1)
        with pytest.raises(TypeError):
            MenuItem("салат", 100)
