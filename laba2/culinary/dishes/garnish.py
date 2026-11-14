"""Гарнир — компонент основного блюда."""

from culinary.exceptions import PortionException
from culinary.ingredients.ingredient import Ingredient
from culinary.validation import require_number, require_text


class Garnish:
    """Гарнир: набор ингредиентов с граммовкой и стилем оформления."""

    STANDARD_WEIGHT = 150

    def __init__(self, name, ingredients=None, weight=STANDARD_WEIGHT, decoration_style="классический"):
        self.__name = require_text(name, "Название гарнира не может быть пустым")
        self.__weight = require_number(weight, "Вес гарнира должен быть положительным", PortionException, positive=True)
        self.__decoration_style = require_text(decoration_style, "Стиль оформления не может быть пустым")
        self.__ingredients = []
        for ingredient, grams in ingredients or []:
            self.add_ingredient(ingredient, grams)

    @property
    def name(self):
        return self.__name

    @property
    def ingredients(self):
        """Пары (ингредиент, граммы)."""
        return tuple(self.__ingredients)

    @property
    def weight(self):
        return self.__weight

    @property
    def decoration_style(self):
        return self.__decoration_style

    def add_ingredient(self, ingredient, grams):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Компонент гарнира должен быть объектом Ingredient")
        require_number(grams, "Граммовка должна быть положительной", PortionException, positive=True)
        if self.calculate_ingredient_weight() + grams > self.__weight:
            raise PortionException("Состав гарнира превышает его заявленный вес")
        self.__ingredients.append((ingredient, grams))

    def calculate_ingredient_weight(self):
        return sum(grams for _, grams in self.__ingredients)

    def is_light_garnish(self, limit=STANDARD_WEIGHT):
        return self.weight <= limit
