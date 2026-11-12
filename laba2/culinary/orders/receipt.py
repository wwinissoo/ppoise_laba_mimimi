from culinary.exceptions import PaymentError
class Receipt:
    """Объект предметной области: Receipt."""

    def __init__(self, order, payment, receipt_number, issued):
        self.__order = order
        self.__payment = payment
        self.__receipt_number = receipt_number
        self.__issued = issued

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
        if not self.payment.is_paid(): raise PaymentError('Нельзя выдать чек без оплаты')
        self.__issued = True
        return self.receipt_number

    def format_total(self):
        return f'{self.order.calculate_total():.2f}'

    def void(self):
        self.__issued = False

