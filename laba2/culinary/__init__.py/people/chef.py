class Chef:
    """Объект предметной области: Chef."""

    def __init__(self, name, phone, email, age, specialization, experience_years):
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__age = age
        self.__specialization = specialization
        self.__experience_years = experience_years

    @property
    def name(self):
        return self.__name

    @property
    def phone(self):
        return self.__phone

    @property
    def email(self):
        return self.__email

    @property
    def age(self):
        return self.__age

    @property
    def specialization(self):
        return self.__specialization

    @property
    def experience_years(self):
        return self.__experience_years

    def prepare_recipe(self, recipe):
        return recipe.estimate_total_cost()

    def can_prepare(self, category):
        return self.specialization == category

    def add_experience(self, years):
        if years < 0: raise ValueError('Стаж не может быть отрицательным')
        self.experience_years += years

