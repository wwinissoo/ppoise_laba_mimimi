from datetime import datetime

from fitness.exceptions import PaymentDeclinedError
from fitness.validation import ensure_choice, ensure_instance, ensure_number, ensure_positive


class Payment:
    """Оплата: наличные (со сдачей) или карта (ровно сумма)."""

    PENDING = "ожидает"
    PAID = "оплачен"
    REFUNDED = "возвращён"
    CASH = "наличные"
    CARD = "карта"

    def __init__(self, amount, method, created_at):
        self._amount = ensure_positive(amount, "сумма")
        self._method = ensure_choice(method, {self.CASH, self.CARD}, "способ оплаты")
        self._created_at = ensure_instance(created_at, datetime, "время создания")
        self._status = self.PENDING
        self._paid_amount = 0

    @property
    def amount(self):
        return self._amount

    @property
    def method(self):
        return self._method

    @property
    def created_at(self):
        return self._created_at

    @property
    def status(self):
        return self._status

    @property
    def paid_amount(self):
        return self._paid_amount

    def pay(self, given_amount):
        """Принимает оплату и возвращает сдачу."""
        if self._status != self.PENDING:
            raise PaymentDeclinedError(f"Платёж уже в статусе «{self._status}»")
        ensure_number(given_amount, "внесённая сумма", minimum=0)
        if given_amount < self._amount:
            raise PaymentDeclinedError(f"Недостаточно средств: нужно {self._amount}")
        if self._method == self.CARD and given_amount != self._amount:
            raise PaymentDeclinedError("По карте списывается ровно сумма платежа")
        self._status = self.PAID
        self._paid_amount = self._amount
        return round(given_amount - self._amount, 2)

    def refund(self):
        if self._status != self.PAID:
            raise PaymentDeclinedError("Вернуть можно только проведённый платёж")
        self._status = self.REFUNDED
        refunded, self._paid_amount = self._paid_amount, 0
        return refunded

    def is_paid(self):
        return self._status == self.PAID
