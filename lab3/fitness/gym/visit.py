from datetime import datetime

from fitness.exceptions import InvalidValueError
from fitness.gym.constants import SECONDS_PER_MINUTE
from fitness.gym.locker import Locker
from fitness.users.user import User
from fitness.validation import ensure_instance


class Visit:
    """Посещение клуба от входа до выхода."""

    def __init__(self, user, checked_in_at, locker=None):
        self._user = ensure_instance(user, User, "посетитель")
        self._checked_in_at = ensure_instance(checked_in_at, datetime, "время входа")
        self._locker = None if locker is None else ensure_instance(locker, Locker, "шкафчик")
        self._checked_out_at = None

    @property
    def user(self):
        return self._user

    @property
    def checked_in_at(self):
        return self._checked_in_at

    @property
    def locker(self):
        return self._locker

    @property
    def checked_out_at(self):
        return self._checked_out_at

    def is_open(self):
        return self._checked_out_at is None

    def check_out(self, now):
        if not self.is_open():
            raise InvalidValueError("Выход уже отмечен")
        if now < self._checked_in_at:
            raise InvalidValueError("Выход не может быть раньше входа")
        self._checked_out_at = now
        if self._locker is not None:
            self._locker.release()

    def duration_minutes(self, now=None):
        end = self._checked_out_at or now or self._checked_in_at
        return round((end - self._checked_in_at).total_seconds() / SECONDS_PER_MINUTE)
