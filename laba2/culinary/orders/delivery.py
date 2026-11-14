"""Доставка клиентского заказа."""

from culinary.exceptions import OrderStateError
from culinary.validation import require_number, require_text, require_transition
from .order import Order


class Delivery:
    """Курьерская доставка готового заказа клиенту."""

    WAITING = "ожидает"
    PREPARING = "готовится"
    IN_TRANSIT = "в пути"
    DELIVERED = "доставлен"
    CANCELLED = "отменён"
    TRANSITIONS = {
        WAITING: {PREPARING, CANCELLED},
        PREPARING: {IN_TRANSIT, CANCELLED},
        IN_TRANSIT: {DELIVERED},
        DELIVERED: set(),
        CANCELLED: set(),
    }
    STATUSES = set(TRANSITIONS)

    def __init__(self, order, address, delivery_fee=0, status=WAITING):
        if not isinstance(order, Order):
            raise TypeError("Доставка должна ссылаться на объект Order")
        if status != self.WAITING:
            raise OrderStateError("Новая доставка должна иметь статус «ожидает»")
        self.__order = order
        self.__address = require_text(address, "Адрес доставки не может быть пустым")
        self.__delivery_fee = require_number(delivery_fee, "Стоимость доставки не может быть отрицательной", minimum=0)
        self.__status = status

    @property
    def order(self):
        return self.__order

    @property
    def address(self):
        return self.__address

    @property
    def delivery_fee(self):
        return self.__delivery_fee

    @property
    def status(self):
        return self.__status

    def calculate_total(self):
        return self.order.calculate_total() + self.delivery_fee

    def update_status(self, status):
        self.__status = require_transition(self.TRANSITIONS, self.__status, status, OrderStateError)

    def is_completed(self):
        return self.status == self.DELIVERED

    def is_cancelled(self):
        return self.status == self.CANCELLED
