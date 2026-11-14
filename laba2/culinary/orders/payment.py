from culinary.exceptions import PaymentError
from culinary.validation import is_number


class Payment:
    """Платеж по заказу, закупке или доставке с однократным переходом статуса."""

    PENDING = "ожидает"
    PAID = "оплачено"
    REFUNDED = "возвращено"
    DECLINED = "отклонено"
    STATUSES = {PENDING, PAID, REFUNDED, DECLINED}
    CASH_METHOD = "наличные"
    METHODS = (CASH_METHOD, "карта", "онлайн")
    FOR_ORDER = "заказ"
    FOR_DELIVERY = "доставка"
    FOR_PURCHASE = "закупка"
    PURPOSES = (FOR_ORDER, FOR_DELIVERY, FOR_PURCHASE)

    def __init__(self, order, amount, method, status=PENDING, purpose=FOR_ORDER, expected_amount=None):
        if not callable(getattr(order, "calculate_total", None)):
            raise TypeError("Платёж должен ссылаться на объект с методом calculate_total")
        self._validate(amount, method, status, purpose, expected_amount)
        self.__order = order
        self.__amount = amount
        self.__method = method
        self.__status = status
        self.__purpose = purpose
        self.__expected_amount = expected_amount
        self.__charged_amount = 0

    @classmethod
    def _validate(cls, amount, method, status, purpose, expected_amount):
        if not is_number(amount) or amount < 0:
            raise PaymentError("Сумма платежа не может быть отрицательной")
        if method not in cls.METHODS:
            raise PaymentError(f"Способ оплаты должен быть одним из: {', '.join(cls.METHODS)}")
        if purpose not in cls.PURPOSES:
            raise PaymentError(f"Назначение платежа должно быть одним из: {', '.join(cls.PURPOSES)}")
        if status != cls.PENDING:
            raise PaymentError("Новый платеж должен иметь статус «ожидает»")
        if expected_amount is not None and (not is_number(expected_amount) or expected_amount < 0):
            raise PaymentError("Ожидаемая сумма платежа указана неверно")

    @property
    def order(self):
        return self.__order

    @property
    def amount(self):
        return self.__amount

    @property
    def method(self):
        return self.__method

    @property
    def status(self):
        return self.__status

    @property
    def purpose(self):
        return self.__purpose

    @property
    def charged_amount(self):
        """Сумма, фактически удержанная после выдачи сдачи."""
        return self.__charged_amount

    @property
    def expected_amount(self):
        if self.__expected_amount is not None:
            return self.__expected_amount
        return self.order.calculate_total()

    def _decline(self, message):
        self.__status = self.DECLINED
        raise PaymentError(message)

    def process(self):
        """Проводит платёж и возвращает сдачу (сдача возможна только при оплате наличными)."""
        if self.status != self.PENDING:
            raise PaymentError("Платеж уже обработан")
        expected = self.expected_amount
        if self.amount < expected:
            self._decline("Недостаточная сумма оплаты")
        if self.method != self.CASH_METHOD and self.amount != expected:
            self._decline("Безналичная оплата проводится только на точную сумму")
        self.__status = self.PAID
        self.__charged_amount = expected
        return self.amount - expected

    def refund(self):
        """Возвращает клиенту удержанную сумму (сдача уже была выдана при оплате)."""
        if self.status != self.PAID:
            raise PaymentError("Можно вернуть только выполненный платеж")
        self.__status = self.REFUNDED
        return self.__charged_amount

    def is_paid(self):
        return self.status == self.PAID

    def is_refunded(self):
        return self.status == self.REFUNDED
