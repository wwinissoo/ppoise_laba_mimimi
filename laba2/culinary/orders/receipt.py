from culinary.exceptions import PaymentError
from culinary.validation import require_text
from .order import Order
from .payment import Payment


class Receipt:
    """Кассовый чек по оплаченному заказу."""

    def __init__(self, order, payment, receipt_number, issued=False):
        if not isinstance(order, Order):
            raise TypeError("Чек должен ссылаться на объект Order")
        if not isinstance(payment, Payment):
            raise TypeError("Чек должен ссылаться на объект Payment")
        if payment.order is not order:
            raise PaymentError("Платёж относится к другому заказу")
        self.__order = order
        self.__payment = payment
        self.__receipt_number = require_text(receipt_number, "Номер чека не может быть пустым")
        self.__issued = False
        if issued:
            self.issue()

    @property
    def order(self):
        return self.__order

    @property
    def payment(self):
        return self.__payment

    @property
    def receipt_number(self):
        return self.__receipt_number

    @property
    def issued(self):
        return self.__issued

    def issue(self):
        if not self.payment.is_paid():
            raise PaymentError("Нельзя выдать чек без оплаты")
        if self.__issued:
            raise PaymentError("Чек уже выдан")
        self.__issued = True
        return self.receipt_number

    def format_total(self):
        return f"{self.payment.charged_amount:.2f}"

    def format_lines(self):
        lines = [f"Чек {self.receipt_number}, заказ {self.order.order_number}"]
        lines += [f"{item.dish.name} × {item.quantity}: {item.calculate_total():.2f}" for item in self.order.items]
        lines.append(f"Итого: {self.format_total()} ({self.payment.method})")
        return lines

    def void(self):
        """Аннулирует выданный чек (допустимо только после возврата платежа)."""
        if not self.__issued:
            raise PaymentError("Нельзя аннулировать невыданный чек")
        if self.payment.is_paid():
            raise PaymentError("Сначала оформите возврат платежа")
        self.__issued = False
