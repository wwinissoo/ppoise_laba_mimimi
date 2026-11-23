from fitness.exceptions import DuplicateEntityError
from fitness.goals.achievement import Achievement
from fitness.users.user import User
from fitness.validation import ensure_instance


class AchievementBoard:
    """Набор достижений пользователя и подсчёт очков."""

    def __init__(self, user):
        self._user = ensure_instance(user, User, "пользователь")
        self._achievements = {}

    @property
    def user(self):
        return self._user

    @property
    def achievements(self):
        return tuple(self._achievements.values())

    def add(self, achievement):
        ensure_instance(achievement, Achievement, "достижение")
        if achievement.code in self._achievements:
            raise DuplicateEntityError(f"Достижение {achievement.code} уже на доске")
        self._achievements[achievement.code] = achievement

    def evaluate(self, metric, value, now):
        """Открывает все подходящие достижения и возвращает новые."""
        return [item for item in self._achievements.values() if item.try_unlock(metric, value, now)]

    def unlocked(self):
        return [item for item in self._achievements.values() if item.is_unlocked()]

    def total_points(self):
        return sum(item.points for item in self.unlocked())

    def completion_percent(self):
        if not self._achievements:
            return 0.0
        return round(len(self.unlocked()) / len(self._achievements) * 100, 1)
