from fitness.exceptions import CapacityExceededError, DuplicateEntityError, EntityNotFoundError
from fitness.users.certification import Certification
from fitness.users.constants import MINUTES_PER_HOUR
from fitness.users.user import User
from fitness.validation import ensure_count, ensure_instance, ensure_positive, ensure_text


class Trainer:
    """Тренер, ведущий клиентов и групповые занятия."""

    def __init__(self, full_name, specializations, hourly_rate, max_clients=10):
        self._full_name = ensure_text(full_name, "ФИО тренера")
        self._specializations = {ensure_text(item, "специализация").casefold() for item in specializations}
        self._hourly_rate = ensure_positive(hourly_rate, "ставка в час")
        self._max_clients = ensure_count(max_clients, "максимум клиентов", minimum=1)
        self._certifications = []
        self._clients = []

    @property
    def full_name(self):
        return self._full_name

    @property
    def specializations(self):
        return tuple(sorted(self._specializations))

    @property
    def hourly_rate(self):
        return self._hourly_rate

    @property
    def max_clients(self):
        return self._max_clients

    @property
    def certifications(self):
        return tuple(self._certifications)

    @property
    def clients(self):
        return tuple(self._clients)

    def add_certification(self, certification):
        self._certifications.append(ensure_instance(certification, Certification, "сертификат"))

    def is_certified(self, on_date):
        return any(item.is_valid(on_date) for item in self._certifications)

    def can_lead(self, workout_type):
        return isinstance(workout_type, str) and workout_type.casefold() in self._specializations

    def assign_client(self, user):
        ensure_instance(user, User, "клиент")
        if user in self._clients:
            raise DuplicateEntityError(f"{user.username} уже клиент тренера")
        if len(self._clients) >= self._max_clients:
            raise CapacityExceededError(f"У тренера {self._full_name} нет свободных мест")
        self._clients.append(user)

    def release_client(self, user):
        if user not in self._clients:
            raise EntityNotFoundError(f"{getattr(user, 'username', user)} не клиент тренера")
        self._clients.remove(user)

    def session_fee(self, minutes):
        ensure_positive(minutes, "длительность")
        return round(self._hourly_rate * minutes / MINUTES_PER_HOUR, 2)
