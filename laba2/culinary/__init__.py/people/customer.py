from person import Person
class Customer(Person):
    """Объект предметной области: Customer."""

    def __init__(self, name, phone, email, age, loyalty_points):
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__age = age
        self.__loyalty_points = loyalty_points

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
    def loyalty_points(self):
        return self.__loyalty_points

    def add_loyalty_points(self, points):
        if points < 0: raise ValueError('Баллы не могут быть отрицательными')
        self.loyalty_points += points

    def spend_loyalty_points(self, points):
        if points < 0 or points > self.loyalty_points: raise ValueError('Недостаточно баллов')
        self.loyalty_points -= points

    def contact_preference(self):
        return 'телефон' if self.phone else 'электронная почта'

