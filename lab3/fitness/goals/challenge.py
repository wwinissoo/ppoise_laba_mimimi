from datetime import date

from fitness.exceptions import CapacityExceededError, ChallengeError, DuplicateEntityError
from fitness.goals.challenge_entry import ChallengeEntry
from fitness.users.user import User
from fitness.validation import ensure_count, ensure_instance, ensure_positive, ensure_text


class Challenge:
    """Челлендж с метрикой, целевым значением и периодом проведения."""

    def __init__(self, title, metric, target_value, starts_on, ends_on, max_participants=100):
        self._title = ensure_text(title, "название челленджа")
        self._metric = ensure_text(metric, "метрика")
        self._target_value = ensure_positive(target_value, "цель")
        self._starts_on = ensure_instance(starts_on, date, "начало")
        self._ends_on = ensure_instance(ends_on, date, "окончание")
        if self._ends_on < self._starts_on:
            raise ChallengeError("Челлендж не может закончиться раньше начала")
        self._max_participants = ensure_count(max_participants, "максимум участников", minimum=2)
        self._entries = {}

    @property
    def title(self):
        return self._title

    @property
    def metric(self):
        return self._metric

    @property
    def target_value(self):
        return self._target_value

    @property
    def starts_on(self):
        return self._starts_on

    @property
    def ends_on(self):
        return self._ends_on

    @property
    def max_participants(self):
        return self._max_participants

    @property
    def participants(self):
        return tuple(entry.user for entry in self._entries.values())

    def is_active(self, today):
        return self._starts_on <= today <= self._ends_on

    def join(self, user, today):
        ensure_instance(user, User, "участник")
        if today > self._ends_on:
            raise ChallengeError("Челлендж уже завершён")
        if user.username in self._entries:
            raise DuplicateEntityError(f"{user.username} уже участвует")
        if len(self._entries) >= self._max_participants:
            raise CapacityExceededError("Все места в челлендже заняты")
        self._entries[user.username] = ChallengeEntry(user)

    def leave(self, user):
        self._entry(user)
        del self._entries[user.username]

    def _entry(self, user):
        entry = self._entries.get(getattr(user, "username", None))
        if entry is None:
            raise ChallengeError("Пользователь не участвует в челлендже")
        return entry

    def record(self, user, value, today):
        if not self.is_active(today):
            raise ChallengeError("Результаты принимаются только во время челленджа")
        return self._entry(user).add(value)

    def leaderboard(self):
        return sorted(self._entries.values(), key=lambda entry: entry.total, reverse=True)

    def finishers(self):
        return [entry.user for entry in self._entries.values() if entry.total >= self._target_value]

    def winner(self, today):
        if today <= self._ends_on:
            raise ChallengeError("Победитель определяется после окончания челленджа")
        board = self.leaderboard()
        return board[0].user if board and board[0].total > 0 else None
