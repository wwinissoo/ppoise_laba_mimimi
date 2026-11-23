from datetime import date, timedelta

from fitness.exceptions import MembershipError, MembershipExpiredError, MembershipFrozenError, PaymentDeclinedError
from fitness.gym.membership_plan import MembershipPlan
from fitness.gym.payment import Payment
from fitness.users.user import User
from fitness.validation import ensure_instance


class Membership:
    """Абонемент пользователя: активация, заморозка, продление, отмена."""

    PENDING = "не активирован"
    ACTIVE = "активен"
    FROZEN = "заморожен"
    CANCELLED = "отменён"
    MAX_FREEZE_DAYS = 30

    def __init__(self, user, plan, start_date):
        self._user = ensure_instance(user, User, "владелец")
        self._plan = ensure_instance(plan, MembershipPlan, "тариф")
        self._start_date = ensure_instance(start_date, date, "дата начала")
        self._end_date = self._start_date + timedelta(days=plan.duration_days())
        self._status = self.PENDING
        self._freezes_used = 0
        self._frozen_since = None
        self._payments = []

    @property
    def user(self):
        return self._user

    @property
    def plan(self):
        return self._plan

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def freezes_used(self):
        return self._freezes_used

    @property
    def payments(self):
        return tuple(self._payments)

    def _accept_payment(self, payment):
        ensure_instance(payment, Payment, "оплата")
        if not payment.is_paid() or payment.amount < self._plan.total_price():
            raise PaymentDeclinedError("Абонемент требует полной проведённой оплаты")
        self._payments.append(payment)

    def activate(self, payment):
        if self._status != self.PENDING:
            raise MembershipError(f"Абонемент уже {self._status}")
        self._accept_payment(payment)
        self._status = self.ACTIVE

    def is_valid(self, on_date):
        return self._status == self.ACTIVE and self._start_date <= on_date < self._end_date

    def require_access(self, on_date):
        if self._status == self.FROZEN:
            raise MembershipFrozenError("Абонемент заморожен")
        if not self.is_valid(on_date):
            raise MembershipExpiredError("Абонемент неактивен или истёк")

    def allows_group_classes(self):
        return self._plan.includes_group_classes

    def freeze(self, on_date):
        self.require_access(on_date)
        if self._freezes_used >= self._plan.max_freezes:
            raise MembershipFrozenError("Лимит заморозок по тарифу исчерпан")
        self._status = self.FROZEN
        self._frozen_since = on_date
        self._freezes_used += 1

    def unfreeze(self, on_date):
        if self._status != self.FROZEN:
            raise MembershipError("Абонемент не заморожен")
        frozen_days = min((on_date - self._frozen_since).days, self.MAX_FREEZE_DAYS)
        self._end_date += timedelta(days=max(0, frozen_days))
        self._status = self.ACTIVE
        self._frozen_since = None
        return frozen_days

    def renew(self, payment):
        if self._status == self.CANCELLED:
            raise MembershipError("Отменённый абонемент нельзя продлить")
        self._accept_payment(payment)
        self._end_date += timedelta(days=self._plan.duration_days())
        return self._end_date

    def cancel(self):
        if self._status == self.CANCELLED:
            raise MembershipError("Абонемент уже отменён")
        self._status = self.CANCELLED

    def days_remaining(self, on_date):
        return max(0, (self._end_date - on_date).days)
