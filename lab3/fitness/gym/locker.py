from fitness.exceptions import CapacityExceededError, InvalidValueError
from fitness.users.user import User
from fitness.validation import ensure_count, ensure_instance


class Locker:
    """Шкафчик в раздевалке."""

    def __init__(self, number):
        self._number = ensure_count(number, "номер шкафчика", minimum=1)
        self._occupant = None

    @property
    def number(self):
        return self._number

    @property
    def occupant(self):
        return self._occupant

    def is_free(self):
        return self._occupant is None

    def assign(self, user):
        ensure_instance(user, User, "посетитель")
        if not self.is_free():
            raise CapacityExceededError(f"Шкафчик №{self._number} занят")
        self._occupant = user

    def release(self):
        if self.is_free():
            raise InvalidValueError(f"Шкафчик №{self._number} уже свободен")
        self._occupant = None
