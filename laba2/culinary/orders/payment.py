from culinary.exceptions import PaymentError
class Payment:
    """Объект предметной области: Payment."""

    def __init__(self, order, amount, method, status):
        self.__order = order
        self.__amount = amount
        self.__method = method
        self.__status = status

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

    def process(self):
        if self.amount < self.order.calculate_total(): raise PaymentError('Недостаточная сумма оплаты')
        self.__status = 'оплачено'
        return self.amount - self.order.calculate_total()

    def refund(self):
        if self.status != 'оплачено': raise PaymentError('Оплата ещё не выполнена')
        self.__status = 'возвращено'
        return self.amount

    def is_paid(self):
        return self.status == 'оплачено'

