import pytest

from culinary.application import CulinarySystem
from culinary.dishes.dish import Dish
from culinary.dishes.menu_item import MenuItem
from culinary.ingredients.vegetable import Vegetable
from culinary.kitchen.kitchen import Kitchen
from culinary.people.customer import Customer
from culinary.recipes.recipe import Recipe
from culinary.warehouse.warehouse import Warehouse


@pytest.fixture
def tomato():
    return Vegetable("Помидор", 1000, 200, 18, 7, 4)


@pytest.fixture
def recipe(tomato):
    recipe = Recipe("Салат", "Овощной салат", 10, 2)
    recipe.add_ingredient(tomato, 200, "г")
    return recipe


@pytest.fixture
def dish(recipe):
    return Dish("Салат", recipe, 2, 12)


@pytest.fixture
def customer():
    return Customer("Анна", "+7 900 000-00-00", "anna@example.com", 24)


@pytest.fixture
def system(tomato, recipe, dish):
    system = CulinarySystem(Warehouse("Склад", "Кухня", [], 100), Kitchen("Кухня"))
    system.add_ingredient(tomato)
    system.add_recipe(recipe)
    system.add_menu_item(MenuItem(dish, 150, True, "салаты"))
    return system
