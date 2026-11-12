from .person import Person

class Chef(Person):
    """Повар; наследует контактные данные и поведение Person."""

    def __init__(self, name, phone, email, age, specialization, experience_years):
        super().__init__(name, phone, email, age)
        if experience_years < 0:
            raise ValueError("Стаж не может быть отрицательным")
        self.__specialization = specialization
        self.__experience_years = experience_years

    @property
    def specialization(self): return self.__specialization
    @property
    def experience_years(self): return self.__experience_years

    def prepare_recipe(self, recipe):
        return recipe.estimate_total_cost()

    def can_prepare(self, category):
        allowed = getattr(self.specialization, "allowed_categories", self.specialization)
        return category in allowed if isinstance(allowed, (list, tuple, set)) else self.specialization == category

    def add_experience(self, years):
        if years < 0: raise ValueError("Стаж не может быть отрицательным")
        self.__experience_years += years
