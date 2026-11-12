from .person import Person

class Customer(Person):
    """Клиент; общие личные данные наследуются от Person."""

    def __init__(self, name, phone, email, age, loyalty_points):
        super().__init__(name, phone, email, age)
        if loyalty_points < 0: raise ValueError("Баллы не могут быть отрицательными")
        self.__loyalty_points = loyalty_points

    @property
    def loyalty_points(self): return self.__loyalty_points

    def add_loyalty_points(self, points):
        if points < 0: raise ValueError("Количество баллов не может быть отрицательным")
        self.__loyalty_points += points

    def spend_loyalty_points(self, points):
        if points < 0 or points > self.__loyalty_points:
            raise ValueError("Недостаточно бонусных баллов")
        self.__loyalty_points -= points
