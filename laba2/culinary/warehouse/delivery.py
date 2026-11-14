"""Совместимый модуль: поставка поставщика; класс переименован, чтобы не конфликтовать с orders.Delivery."""

from .supplier_delivery import SupplierDelivery

Delivery = SupplierDelivery
__all__ = ["SupplierDelivery", "Delivery"]
