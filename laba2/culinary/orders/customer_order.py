class CustomerOrder:
    """Объект предметной области: CustomerOrder."""

    def __init__(self, customer, order, delivery_address, delivery_required):
        self.__customer = customer
        self.__order = order
        self.__delivery_address = delivery_address
        self.__delivery_required = delivery_required

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
        if not address.strip(): raise ValueError('Адрес не может быть пустым')
        self.__delivery_address = address
        self.__delivery_required = True

    def cancel_delivery(self):
        self.__delivery_required = False

    def get_customer_name(self):
        return self.customer.name

