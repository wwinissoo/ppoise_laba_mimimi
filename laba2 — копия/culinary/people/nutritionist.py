"""Специалист по питанию."""

from culinary.nutrition.diet_plan import DietPlan
from culinary.validation import require_text
from .person import Person


class Nutritionist(Person):
    def __init__(self, name, phone, email, age, qualification, experience_years=0):
        super().__init__(name, phone, email, age)
        if not isinstance(experience_years, int) or experience_years < 0:
            raise ValueError("Стаж не может быть отрицательным")
        self.__qualification = require_text(qualification, "Квалификация не может быть пустой")
        self.__experience_years = experience_years

    @property
    def qualification(self):
        return self.__qualification

    @property
    def experience_years(self):
        return self.__experience_years

    def review_plan(self, plan):
        """План одобряется, если суммарная калорийность приёмов пищи не превышает лимит."""
        if not isinstance(plan, DietPlan):
            raise TypeError("Ожидается объект DietPlan")
        return plan.is_within_limit()

    def add_experience(self, years):
        if not isinstance(years, int) or years <= 0:
            raise ValueError("Добавляемый стаж должен быть положительным")
        self.__experience_years += years
