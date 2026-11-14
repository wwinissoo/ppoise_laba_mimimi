from culinary.exceptions import InvalidOrderException
from culinary.people.customer import Customer
from culinary.validation import require_text
from .order import Order


class CustomerOrder:
    """Связка «клиент — заказ» с параметрами доставки."""

    def __init__(self, customer, order, delivery_address="", delivery_required=False):
        if not isinstance(customer, Customer):
            raise TypeError("Ожидается объект Customer")
        if not isinstance(order, Order):
            raise TypeError("Ожидается объект Order")
        if order.customer is not customer:
            raise InvalidOrderException("Заказ оформлен на другого клиента")
        self.__customer = customer
        self.__order = order
        self.__delivery_address = ""
        self.__delivery_required = False
        if delivery_required:
            self.request_delivery(delivery_address)

    @property
    def customer(self):
        return self.__customer

    @property
    def order(self):
        return self.__order

    @property
    def delivery_address(self):
        return self.__delivery_address

    @property
    def delivery_required(self):
        return self.__delivery_required

    def request_delivery(self, address):
        self.__delivery_address = require_text(address, "Адрес не может быть пустым")
        self.__delivery_required = True

    def cancel_delivery(self):
        self.__delivery_required = False
        self.__delivery_address = ""

    def get_customer_name(self):
        return self.customer.name
