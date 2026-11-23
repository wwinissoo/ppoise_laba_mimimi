from datetime import datetime

from fitness.exceptions import GoalStateError
from fitness.validation import ensure_count, ensure_instance, ensure_positive, ensure_text


class Achievement:
    """Бейдж, открывающийся при достижении порога метрики."""

    def __init__(self, code, title, metric, threshold, points=10):
        self._code = ensure_text(code, "код достижения").upper()
        self._title = ensure_text(title, "название достижения")
        self._metric = ensure_text(metric, "метрика")
        self._threshold = ensure_positive(threshold, "порог")
        self._points = ensure_count(points, "очки", minimum=1)
        self._unlocked_at = None

    @property
    def code(self):
        return self._code

    @property
    def title(self):
        return self._title

    @property
    def metric(self):
        return self._metric

    @property
    def threshold(self):
        return self._threshold

    @property
    def points(self):
        return self._points

    @property
    def unlocked_at(self):
        return self._unlocked_at

    def is_unlocked(self):
        return self._unlocked_at is not None

    def unlock(self, now):
        if self.is_unlocked():
            raise GoalStateError(f"Достижение «{self._title}» уже получено")
        self._unlocked_at = ensure_instance(now, datetime, "время получения")

    def try_unlock(self, metric, value, now):
        if self.is_unlocked() or metric != self._metric or value < self._threshold:
            return False
        self.unlock(now)
        return True
