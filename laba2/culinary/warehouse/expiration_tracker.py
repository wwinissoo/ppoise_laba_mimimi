"""Отслеживание сроков годности складских ингредиентов."""

from culinary.ingredients.ingredient import Ingredient


class ExpirationTracker:
    def __init__(self, ingredients=None):
        self.__ingredients = []
        for ingredient in ingredients or []:
            self.register(ingredient)

    @property
    def ingredients(self):
        return tuple(self.__ingredients)

    def register(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Ожидается объект Ingredient")
        if ingredient not in self.__ingredients:
            self.__ingredients.append(ingredient)

    def advance_day(self):
        for ingredient in self.__ingredients:
            ingredient.pass_day()

    def expired_items(self):
        return [item for item in self.__ingredients if not item.check_expiration()]

    def fresh_items(self):
        return [item for item in self.__ingredients if item.check_expiration()]

    def expiring_within(self, days):
        """Свежие ингредиенты, срок которых истечёт не позже чем через days дней."""
        return [item for item in self.fresh_items() if item.expiration_days - item.days_passed <= days]
