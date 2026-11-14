from culinary.units import ADULT_AGE
import re

from culinary.validation import require_text


class Person:
    """Участник системы с контактными данными."""

    MAX_AGE = 120
    PHONE_PATTERN = re.compile(r"^\+?[\d\s()\-]{5,20}$")
    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, name, phone, email, age):
        self.__name = require_text(name, "Имя не может быть пустым")
        self.__phone = self._validate_phone(phone)
        self.__email = self._validate_email(email)
        if not isinstance(age, int) or isinstance(age, bool) or not 0 <= age <= self.MAX_AGE:
            raise ValueError(f"Возраст должен быть целым числом от 0 до {self.MAX_AGE}")
        self.__age = age
        if not self.has_valid_contact():
            raise ValueError("Нужно указать телефон или электронную почту")

    @classmethod
    def _validate_phone(cls, phone):
        phone = str(phone or "").strip()
        if phone and not cls.PHONE_PATTERN.match(phone):
            raise ValueError("Некорректный номер телефона")
        return phone

    @classmethod
    def _validate_email(cls, email):
        email = str(email or "").strip()
        if email and not cls.EMAIL_PATTERN.match(email):
            raise ValueError("Некорректный адрес электронной почты")
        return email

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
        phone = self._validate_phone(phone)
        if not phone and not self.__email:
            raise ValueError("Нельзя удалить единственный контакт")
        self.__phone = phone

    def has_valid_contact(self):
        return bool(self.phone or self.email)

    def is_adult(self):
        return self.age >= ADULT_AGE
