"""Специалист по питанию."""
from .person import Person
class Nutritionist(Person):
    def __init__(self,name,phone,email,age,qualification,experience_years=0):
        super().__init__(name,phone,email,age)
        if experience_years < 0: raise ValueError("Стаж не может быть отрицательным")
        self.__qualification=qualification; self.__experience_years=experience_years
    @property
    def qualification(self): return self.__qualification
    @property
    def experience_years(self): return self.__experience_years
    def review_plan(self,plan): return plan.daily_calorie_limit > 0
    def add_experience(self,years):
        if years <= 0: raise ValueError("Добавляемый стаж должен быть положительным")
        self.__experience_years+=years
