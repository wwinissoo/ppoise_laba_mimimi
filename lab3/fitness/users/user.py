from datetime import date

from fitness.exceptions import DuplicateEntityError, InvalidCredentialsError, InvalidValueError
from fitness.users.body_measurement import BodyMeasurement
from fitness.users.health_profile import HealthProfile
from fitness.users.password_policy import PasswordPolicy
from fitness.users.user_settings import UserSettings
from fitness.validation import ensure_choice, ensure_instance, ensure_text


class User:
    """Зарегистрированный пользователь с историей замеров тела."""

    MALE = "м"
    FEMALE = "ж"
    GENDERS = {MALE, FEMALE}
    MIN_AGE = 10

    def __init__(self, username, email, password_hash, salt, birth_date, gender, health_profile=None, settings=None):
        self._username = ensure_text(username, "логин")
        self._email = self._validate_email(email)
        self._password_hash = ensure_text(password_hash, "хэш пароля")
        self._salt = ensure_text(salt, "соль")
        self._birth_date = ensure_instance(birth_date, date, "дата рождения")
        self._gender = ensure_choice(gender, self.GENDERS, "пол")
        self._health_profile = ensure_instance(health_profile or HealthProfile(70), HealthProfile, "профиль здоровья")
        self._settings = ensure_instance(settings or UserSettings(), UserSettings, "настройки")
        self._measurements = []

    @classmethod
    def register(cls, username, email, raw_password, birth_date, gender, policy):
        ensure_instance(policy, PasswordPolicy, "политика паролей")
        policy.validate(raw_password)
        salt = policy.generate_salt()
        return cls(username, email, policy.hash_password(raw_password, salt), salt, birth_date, gender)

    @staticmethod
    def _validate_email(email):
        text = ensure_text(email, "e-mail")
        local, _, domain = text.partition("@")
        if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise InvalidValueError(f"Некорректный e-mail «{text}»")
        return text.lower()

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def gender(self):
        return self._gender

    @property
    def health_profile(self):
        return self._health_profile

    @property
    def settings(self):
        return self._settings

    @property
    def measurements(self):
        return tuple(self._measurements)

    def age(self, today=None):
        today = today or date.today()
        had_birthday = (today.month, today.day) >= (self._birth_date.month, self._birth_date.day)
        return today.year - self._birth_date.year - (0 if had_birthday else 1)

    def verify_password(self, raw_password):
        return PasswordPolicy.matches(raw_password, self._salt, self._password_hash)

    def change_password(self, old_password, new_password, policy):
        if not self.verify_password(old_password):
            raise InvalidCredentialsError("Текущий пароль указан неверно")
        if old_password == new_password:
            raise InvalidValueError("Новый пароль должен отличаться от старого")
        policy.validate(new_password)
        self._salt = policy.generate_salt()
        self._password_hash = policy.hash_password(new_password, self._salt)

    def update_email(self, email):
        self._email = self._validate_email(email)

    def add_measurement(self, measurement):
        ensure_instance(measurement, BodyMeasurement, "замер")
        if any(item.measured_on == measurement.measured_on for item in self._measurements):
            raise DuplicateEntityError(f"Замер за {measurement.measured_on} уже есть")
        self._measurements.append(measurement)
        self._measurements.sort(key=lambda item: item.measured_on)

    def latest_measurement(self):
        return self._measurements[-1] if self._measurements else None

    def weight_change(self):
        if len(self._measurements) < 2:
            return 0.0
        return self._measurements[-1].weight_difference(self._measurements[0])
