from person import Person
class KitchenWorker(Person):
    """Объект предметной области: KitchenWorker."""

    def __init__(self, name, phone, email, age, position, shift_hours):
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__age = age
        self.__position = position
        self.__shift_hours = shift_hours

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
    def position(self):
        return self.__position

    @property
    def shift_hours(self):
        return self.__shift_hours

    def change_shift(self, hours):
        if hours <= 0: raise ValueError('Продолжительность смены должна быть положительной')
        self.shift_hours = hours

    def is_shift_long(self, limit=8):
        return self.shift_hours > limit

    def describe_position(self):
        return f'{self.name}: {self.position}'

