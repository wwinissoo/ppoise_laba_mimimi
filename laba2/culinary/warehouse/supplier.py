from culinary.exceptions import SupplierError
from culinary.ingredients.ingredient import Ingredient
from culinary.validation import require_text


class Supplier:
    """Поставщик ингредиентов с ассортиментом и рейтингом (0 — ещё не оценён)."""

    MIN_RATING = 1
    MAX_RATING = 5
    RELIABLE_RATING = 4

    def __init__(self, name, phone, products=None, rating=0):
        self.__name = require_text(name, "Название поставщика не может быть пустым", SupplierError)
        self.__phone = require_text(phone, "Телефон поставщика не может быть пустым", SupplierError)
        if rating != 0 and not self.MIN_RATING <= rating <= self.MAX_RATING:
            raise SupplierError("Оценка поставщика должна быть 0 (нет оценки) или от 1 до 5")
        self.__rating = rating
        self.__products = []
        for ingredient in products or []:
            self.add_product(ingredient)

    @property
    def name(self):
        return self.__name

    @property
    def phone(self):
        return self.__phone

    @property
    def products(self):
        return tuple(self.__products)

    @property
    def rating(self):
        return self.__rating

    def add_product(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Ассортимент поставщика состоит из объектов Ingredient")
        if not self.supplies(ingredient):
            self.__products.append(ingredient)

    def rate(self, score):
        if not self.MIN_RATING <= score <= self.MAX_RATING:
            raise SupplierError("Оценка поставщика должна быть от 1 до 5")
        self.__rating = score

    def is_reliable(self, minimum=RELIABLE_RATING):
        return self.__rating >= minimum

    def supplies(self, ingredient):
        name = getattr(ingredient, "name", str(ingredient)).strip().casefold()
        return any(item.name.casefold() == name for item in self.__products)
