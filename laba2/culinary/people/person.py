class Person:
    """Объект предметной области: Person."""

    def __init__(self, name, phone, email, age):
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__age = age

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

    def change_phone(self, phone):
        self.__phone = phone

    def has_valid_contact(self):
        return bool(self.phone or self.email)

    def is_adult(self):
        return self.age >= 18

