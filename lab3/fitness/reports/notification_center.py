from fitness.exceptions import ScheduleConflictError
from fitness.reports.notification import Notification
from fitness.reports.reminder import Reminder
from fitness.users.user import User
from fitness.validation import ensure_instance


class NotificationCenter:
    """Уведомления и напоминания пользователя с учётом его настроек."""

    def __init__(self, user):
        self._user = ensure_instance(user, User, "пользователь")
        self._notifications = []
        self._reminders = []

    @property
    def user(self):
        return self._user

    @property
    def notifications(self):
        return tuple(self._notifications)

    @property
    def reminders(self):
        return tuple(self._reminders)

    def push(self, notification):
        ensure_instance(notification, Notification, "уведомление")
        if not self._user.settings.notifications_enabled:
            return False
        self._notifications.append(notification)
        return True

    def add_reminder(self, reminder):
        ensure_instance(reminder, Reminder, "напоминание")
        if any(item.clashes_with(reminder) for item in self._reminders):
            raise ScheduleConflictError("На это время уже есть напоминание")
        self._reminders.append(reminder)

    def process_reminders(self, now):
        """Создаёт уведомления по наступившим напоминаниям."""
        fired = []
        for reminder in self._reminders:
            if reminder.is_due(now):
                reminder.mark_fired(now)
                notification = Notification("Напоминание", reminder.message, now)
                if self.push(notification):
                    fired.append(notification)
        return fired

    def unread_count(self):
        return sum(1 for item in self._notifications if not item.read)

    def mark_all_read(self):
        for item in self._notifications:
            item.mark_read()

    def clear_read(self):
        before = len(self._notifications)
        self._notifications = [item for item in self._notifications if not item.read]
        return before - len(self._notifications)
