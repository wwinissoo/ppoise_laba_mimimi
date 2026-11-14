from culinary.nutrition.allergen import Allergen
from culinary.validation import require_number
from .person import Person


class Customer(Person):
    """Клиент; общие личные данные наследуются от Person."""

    POINTS_PER_RUBLE = 0.05

    def __init__(self, name, phone, email, age, loyalty_points=0, allergies=None):
        super().__init__(name, phone, email, age)
        if not isinstance(loyalty_points, int) or isinstance(loyalty_points, bool) or loyalty_points < 0:
            raise ValueError("Баллы должны быть неотрицательным целым числом")
        self.__loyalty_points = loyalty_points
        self.__allergies = []
        for allergen in allergies or []:
            self.add_allergy(allergen)

    @property
    def loyalty_points(self):
        return self.__loyalty_points

    @property
    def allergies(self):
        return tuple(self.__allergies)

    def add_loyalty_points(self, points):
        if not isinstance(points, int) or isinstance(points, bool) or points < 0:
            raise ValueError("Количество баллов должно быть неотрицательным целым числом")
        self.__loyalty_points += points

    def spend_loyalty_points(self, points):
        if not isinstance(points, int) or points < 0 or points > self.__loyalty_points:
            raise ValueError("Недостаточно бонусных баллов")
        self.__loyalty_points -= points

    def earn_points_for_purchase(self, amount):
        require_number(amount, "Сумма покупки не может быть отрицательной", minimum=0)
        points = int(amount * self.POINTS_PER_RUBLE)
        self.__loyalty_points += points
        return points

    def add_allergy(self, allergen):
        if not isinstance(allergen, Allergen):
            raise TypeError("Аллергия должна быть объектом Allergen")
        if all(item.name.casefold() != allergen.name.casefold() for item in self.__allergies):
            self.__allergies.append(allergen)

    def ensure_can_eat(self, dish):
        """Вызывает AllergenException, если блюдо содержит аллерген клиента."""
        for allergen in self.__allergies:
            allergen.ensure_absent(dish.recipe)
        return True
