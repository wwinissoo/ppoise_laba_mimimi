from datetime import datetime

from culinary.exceptions import InvalidOrderException, OrderStateError
from culinary.people.customer import Customer
from culinary.validation import require_transition
from .order_item import OrderItem


class Order:
    """Заказ с проверяемыми переходами статуса и редактированием до приготовления."""

    NEW = "новый"
    COOKING = "готовится"
    READY = "готов"
    HANDED_OVER = "выдан"
    CANCELLED = "отменён"
    TRANSITIONS = {
        NEW: {COOKING, CANCELLED},
        COOKING: {READY, CANCELLED},
        READY: {HANDED_OVER},
        HANDED_OVER: set(),
        CANCELLED: set(),
    }
    STATUSES = set(TRANSITIONS)

    def __init__(self, order_number, customer, items, status=NEW, created_at=None):
        if not isinstance(order_number, str) or not order_number.strip():
            raise OrderStateError("Номер заказа не может быть пустым")
        if status != self.NEW:
            raise OrderStateError("Новый заказ должен иметь статус «новый»")
        if not isinstance(customer, Customer):
            raise TypeError("Заказчик должен быть объектом Customer")
        if created_at is not None and not isinstance(created_at, datetime):
            raise TypeError("Дата создания заказа должна быть datetime")
        self.__order_number = order_number.strip()
        self.__customer = customer
        self.__items = self._validate_items(items)
        self.__status = status
        self.__created_at = created_at or datetime.now()

    @staticmethod
    def _validate_items(items):
        if not isinstance(items, (list, tuple)) or any(not isinstance(item, OrderItem) for item in items):
            raise TypeError("Позиции заказа должны быть списком объектов OrderItem")
        if not items:
            raise InvalidOrderException("Заказ должен содержать хотя бы одну позицию")
        return list(items)

    @property
    def order_number(self):
        return self.__order_number

    @property
    def customer(self):
        return self.__customer

    @property
    def items(self):
        return tuple(self.__items)

    @property
    def status(self):
        return self.__status

    @property
    def created_at(self):
        return self.__created_at

    def add_item(self, item):
        self._require_editable()
        if not isinstance(item, OrderItem):
            raise TypeError("В заказ можно добавить только OrderItem")
        self.__items.append(item)

    def remove_item(self, item):
        self._require_editable()
        if item not in self.__items:
            return False
        if len(self.__items) == 1:
            raise InvalidOrderException("Нельзя удалить последнюю позицию заказа")
        self.__items.remove(item)
        return True

    def replace_items(self, items):
        self._require_editable()
        self.__items = self._validate_items(items)

    def _require_editable(self):
        if self.__status != self.NEW:
            raise OrderStateError("Можно редактировать только новый заказ")

    def calculate_total(self):
        return sum(item.calculate_total() for item in self.__items)

    def count_portions(self):
        return sum(item.quantity for item in self.__items)

    def change_status(self, status):
        self.__status = require_transition(self.TRANSITIONS, self.__status, status, OrderStateError)
