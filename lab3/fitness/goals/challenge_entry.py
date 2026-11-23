from fitness.users.user import User
from fitness.validation import ensure_instance, ensure_number


class ChallengeEntry:
    """Результат одного участника челленджа."""

    def __init__(self, user):
        self._user = ensure_instance(user, User, "участник")
        self._total = 0
        self._contributions = 0

    @property
    def user(self):
        return self._user

    @property
    def total(self):
        return self._total

    @property
    def contributions(self):
        return self._contributions

    def add(self, value):
        self._total += ensure_number(value, "результат", minimum=0)
        self._contributions += 1
        return self._total
