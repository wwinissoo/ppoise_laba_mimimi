from datetime import datetime, timedelta

from fitness.exceptions import DuplicateEntityError, EntityNotFoundError, MembershipError, ScheduleConflictError
from fitness.gym.membership import Membership
from fitness.users.trainer import Trainer
from fitness.validation import ensure_count, ensure_instance, ensure_positive, ensure_text


class GroupClass:
    """Групповая тренировка (йога, сайкл, функциональный тренинг)."""

    def __init__(self, title, trainer, workout_type, starts_at, duration_minutes, capacity):
        self._title = ensure_text(title, "название занятия")
        self._trainer = ensure_instance(trainer, Trainer, "тренер")
        self._workout_type = ensure_text(workout_type, "тип тренировки")
        if not trainer.can_lead(self._workout_type):
            raise ScheduleConflictError(f"{trainer.full_name} не ведёт «{self._workout_type}»")
        self._starts_at = ensure_instance(starts_at, datetime, "начало")
        self._duration_minutes = ensure_positive(duration_minutes, "длительность")
        self._capacity = ensure_count(capacity, "вместимость", minimum=1)
        self._attendees = []
        self._waitlist = []

    @property
    def title(self):
        return self._title

    @property
    def trainer(self):
        return self._trainer

    @property
    def workout_type(self):
        return self._workout_type

    @property
    def starts_at(self):
        return self._starts_at

    @property
    def duration_minutes(self):
        return self._duration_minutes

    @property
    def capacity(self):
        return self._capacity

    @property
    def attendees(self):
        return tuple(self._attendees)

    @property
    def waitlist(self):
        return tuple(self._waitlist)

    def ends_at(self):
        return self._starts_at + timedelta(minutes=self._duration_minutes)

    def available_spots(self):
        return self._capacity - len(self._attendees)

    def is_full(self):
        return self.available_spots() == 0

    def book(self, membership):
        """Записывает на занятие; при отсутствии мест — в лист ожидания. True — запись подтверждена."""
        ensure_instance(membership, Membership, "абонемент")
        membership.require_access(self._starts_at.date())
        if not membership.allows_group_classes():
            raise MembershipError("Тариф не включает групповые занятия")
        user = membership.user
        if user in self._attendees or user in self._waitlist:
            raise DuplicateEntityError(f"{user.username} уже записан")
        if self.is_full():
            self._waitlist.append(user)
            return False
        self._attendees.append(user)
        return True

    def cancel_booking(self, user):
        """Отменяет запись; первый из листа ожидания получает место."""
        if user in self._waitlist:
            self._waitlist.remove(user)
            return None
        if user not in self._attendees:
            raise EntityNotFoundError("Пользователь не записан на занятие")
        self._attendees.remove(user)
        if self._waitlist:
            promoted = self._waitlist.pop(0)
            self._attendees.append(promoted)
            return promoted
        return None

    def conflicts_with(self, other):
        ensure_instance(other, GroupClass, "занятие")
        same_trainer = other.trainer is self._trainer
        return same_trainer and self._starts_at < other.ends_at() and other.starts_at < self.ends_at()
