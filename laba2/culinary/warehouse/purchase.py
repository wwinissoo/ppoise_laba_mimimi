"""Закупка ингредиентов у поставщика."""

from culinary.exceptions import OrderStateError, SupplierError
from culinary.ingredients.ingredient import Ingredient
from culinary.validation import is_number, require_transition
from .supplier import Supplier


class Purchase:
    """Закупка партии ингредиента у поставщика: оплата → получение или отмена."""

    AWAITING_PAYMENT = "ожидает оплаты"
    PAID = "оплачена"
    RECEIVED = "получена"
    CANCELLED = "отменена"
    TRANSITIONS = {
        AWAITING_PAYMENT: {PAID, CANCELLED},
        PAID: {RECEIVED, CANCELLED},
        RECEIVED: set(),
        CANCELLED: set(),
    }
    STATUSES = set(TRANSITIONS)

    def __init__(self, supplier, ingredient, quantity_kg, unit_price):
        if not isinstance(supplier, Supplier):
            raise TypeError("Ожидается объект Supplier")
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Ожидается объект Ingredient")
        if not supplier.supplies(ingredient):
            raise SupplierError(f"Поставщик «{supplier.name}» не поставляет «{ingredient.name}»")
        if not is_number(quantity_kg) or not is_number(unit_price) or quantity_kg <= 0 or unit_price < 0:
            raise ValueError("Некорректные параметры закупки")
        self.__supplier = supplier
        self.__ingredient = ingredient
        self.__quantity_kg = quantity_kg
        self.__unit_price = unit_price
        self.__status = self.AWAITING_PAYMENT

    @property
    def supplier(self):
        return self.__supplier

    @property
    def ingredient(self):
        return self.__ingredient

    @property
    def quantity_kg(self):
        return self.__quantity_kg

    @property
    def unit_price(self):
        return self.__unit_price

    @property
    def received(self):
        return self.__status == self.RECEIVED

    @property
    def status(self):
        return self.__status

    def calculate_total(self):
        return self.quantity_kg * self.unit_price

    def _change_status(self, status):
        if status == self.__status:
            raise OrderStateError(f"Закупка уже в статусе «{status}»")
        self.__status = require_transition(self.TRANSITIONS, self.__status, status, OrderStateError)

    def mark_paid(self):
        self._change_status(self.PAID)

    def mark_received(self):
        self._change_status(self.RECEIVED)

    def cancel(self):
        self._change_status(self.CANCELLED)
