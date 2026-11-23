from datetime import datetime

from fitness.reports.constants import SECONDS_PER_MINUTE
from fitness.validation import ensure_instance, ensure_text


class Notification:
    """Уведомление для пользователя."""

    def __init__(self, title, body, created_at):
        self._title = ensure_text(title, "заголовок")
        self._body = ensure_text(body, "текст уведомления")
        self._created_at = ensure_instance(created_at, datetime, "время создания")
        self._read = False

    @property
    def title(self):
        return self._title

    @property
    def body(self):
        return self._body

    @property
    def created_at(self):
        return self._created_at

    @property
    def read(self):
        return self._read

    def mark_read(self):
        self._read = True

    def age_minutes(self, now):
        return int((now - self._created_at).total_seconds() // SECONDS_PER_MINUTE)
