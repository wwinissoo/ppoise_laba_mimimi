"""Соус — компонент блюда (например, заправка салата)."""

from culinary.ingredients.ingredient import Ingredient
from culinary.validation import require_number, require_text


class Sauce:
    """Соус на основе одного базового ингредиента."""

    CONSISTENCIES = ("жидкий", "средний", "густой")

    def __init__(self, name, base_ingredient, consistency="средний", volume=100):
        self.__name = require_text(name, "Название соуса не может быть пустым")
        if not isinstance(base_ingredient, Ingredient):
            raise TypeError("Основа соуса должна быть объектом Ingredient")
        if consistency not in self.CONSISTENCIES:
            raise ValueError(f"Консистенция должна быть одной из: {', '.join(self.CONSISTENCIES)}")
        self.__base_ingredient = base_ingredient
        self.__consistency = consistency
        self.__volume = require_number(volume, "Объём соуса должен быть положительным", positive=True)

    @property
    def name(self):
        return self.__name

    @property
    def base_ingredient(self):
        return self.__base_ingredient

    @property
    def consistency(self):
        return self.__consistency

    @property
    def volume(self):
        return self.__volume

    def thicken(self, amount):
        require_number(amount, "Количество загустителя должно быть положительным", positive=True)
        self.__volume += amount
        self.__consistency = "густой"

    def dilute(self, amount):
        require_number(amount, "Количество жидкости должно быть положительным", positive=True)
        self.__volume += amount
        self.__consistency = "жидкий"

    def reduce(self, amount):
        """Уваривание: объём уменьшается, соус густеет."""
        require_number(amount, "Объём уваривания должен быть положительным", positive=True)
        if amount >= self.__volume:
            raise ValueError("Нельзя уварить весь соус")
        self.__volume -= amount
        self.__consistency = "густой"

    def is_based_on(self, ingredient):
        return self.base_ingredient is ingredient
