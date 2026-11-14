from culinary.exceptions import CulinaryError
from culinary.recipes.recipe import Recipe
from .chef_specialization import ChefSpecialization
from .person import Person


class Chef(Person):
    """Шеф-повар со специализацией; наследует контактные данные и поведение Person."""

    def __init__(self, name, phone, email, age, specialization, experience_years):
        super().__init__(name, phone, email, age)
        if not isinstance(specialization, ChefSpecialization):
            raise TypeError("Специализация должна быть объектом ChefSpecialization")
        if not isinstance(experience_years, int) or isinstance(experience_years, bool) or experience_years < 0:
            raise ValueError("Стаж должен быть неотрицательным целым числом")
        self.__specialization = specialization
        self.__experience_years = experience_years

    @property
    def specialization(self):
        return self.__specialization

    @property
    def experience_years(self):
        return self.__experience_years

    def is_qualified(self):
        return self.specialization.experience_requirement_met(self.experience_years)

    def can_prepare(self, category):
        return self.is_qualified() and self.specialization.allows(category)

    def prepare_recipe(self, recipe, category):
        """Проверяет допуск шефа к категории и возвращает себестоимость рецепта."""
        if not isinstance(recipe, Recipe):
            raise TypeError("Ожидается объект Recipe")
        if not self.can_prepare(category):
            raise CulinaryError(f"Шеф «{self.name}» не допущен к категории «{category}»")
        return recipe.estimate_total_cost()

    def add_experience(self, years):
        if not isinstance(years, int) or years < 0:
            raise ValueError("Стаж не может быть отрицательным")
        self.__experience_years += years
