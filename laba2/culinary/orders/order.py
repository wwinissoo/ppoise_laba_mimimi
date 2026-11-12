from culinary.exceptions import OrderStateError
class Order:
    """Объект предметной области: Order."""

    def __init__(self, order_number, customer, items, status, created_at):
        self.__order_number = order_number
        self.__customer = customer
        self.__items = items
        self.__status = status
        self.__created_at = created_at

    @property
    def order_number(self):
        return self.__order_number

    @property
    def customer(self):
        return self.__customer

    @property
    def items(self):
        return self.__items

    @property
    def status(self):
        return self.__status

    @property
    def created_at(self):
        return self.__created_at

    def add_item(self, item):
        from .order_item import OrderItem
        if not isinstance(item, OrderItem):
            raise TypeError("В заказ можно добавить только OrderItem")
        self.__items.append(item)

    def calculate_total(self):
        return sum(item.calculate_total() for item in self.items)

    def change_status(self, status):
        allowed = {'новый', 'готовится', 'готов', 'выдан', 'отменён'}
        if status not in allowed: raise OrderStateError('Неизвестный статус заказа')
        transitions = {'новый': {'готовится', 'отменён'}, 'готовится': {'готов', 'отменён'}, 'готов': {'выдан'}, 'выдан': set(), 'отменён': set()}
        if status != self.__status and status not in transitions.get(self.__status, set()):
            raise OrderStateError(f'Нельзя изменить статус с «{self.__status}» на «{status}»')
        self.__status = status

