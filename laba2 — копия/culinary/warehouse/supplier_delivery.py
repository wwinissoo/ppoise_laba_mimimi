"""Поставка партий продуктов от поставщика на склад."""

from datetime import date

from culinary.exceptions import SupplierError
from .product_batch import ProductBatch
from .supplier import Supplier


class SupplierDelivery:
    """Поставка от поставщика: создана → в пути → получена (или отменена)."""

    STATUSES = {"создана", "в пути", "получена", "отменена"}
    TRANSITIONS = {
        "создана": {"в пути", "получена", "отменена"},
        "в пути": {"получена", "отменена"},
        "получена": set(),
        "отменена": set(),
    }

    def __init__(self, supplier, batches=None, delivery_date=None, status="создана"):
        if not isinstance(supplier, Supplier):
            raise TypeError("Ожидается объект Supplier")
        if status != "создана":
            raise SupplierError("Новая поставка должна иметь статус «создана»")
        if delivery_date is not None and not isinstance(delivery_date, date):
            raise TypeError("Дата поставки должна быть объектом date")
        self.__supplier = supplier
        self.__delivery_date = delivery_date or date.today()
        self.__status = status
        self.__batches = []
        for batch in batches or []:
            self.add_batch(batch)

    @property
    def supplier(self):
        return self.__supplier

    @property
    def batches(self):
        return tuple(self.__batches)

    @property
    def delivery_date(self):
        return self.__delivery_date

    @property
    def status(self):
        return self.__status

    def _change_status(self, status):
        if status not in self.TRANSITIONS[self.__status]:
            raise SupplierError(f"Нельзя перевести поставку из «{self.__status}» в «{status}»")
        self.__status = status

    def add_batch(self, batch):
        if self.__status not in {"создана", "в пути"}:
            raise SupplierError("Нельзя менять состав завершенной поставки")
        if not isinstance(batch, ProductBatch):
            raise TypeError("Поставка состоит из объектов ProductBatch")
        if batch.supplier is not self.__supplier:
            raise SupplierError("Партия принадлежит другому поставщику")
        if any(item.batch_code == batch.batch_code for item in self.__batches):
            raise SupplierError(f"Партия {batch.batch_code} уже добавлена")
        self.__batches.append(batch)

    def dispatch(self):
        if not self.__batches:
            raise SupplierError("Нельзя отправить пустую поставку")
        self._change_status("в пути")

    def mark_received(self):
        if not self.__batches:
            raise SupplierError("Нельзя принять пустую поставку")
        self._change_status("получена")

    def cancel(self):
        self._change_status("отменена")

    def calculate_delivered_weight(self):
        return sum(batch.quantity_kg for batch in self.__batches)
