from culinary.exceptions import SupplierError
class Delivery:
    """Объект предметной области: Delivery."""

    def __init__(self, supplier, batches, delivery_date, status):
        self.__supplier = supplier
        self.__batches = batches
        self.__delivery_date = delivery_date
        self.__status = status

    @property
    def supplier(self):
        return self.__supplier

    @property
    def batches(self):
        return self.__batches

    @property
    def delivery_date(self):
        return self.__delivery_date

    @property
    def status(self):
        return self.__status

    def add_batch(self, batch):
        self.batches.append(batch)

    def mark_received(self):
        if self.__status not in {'создана', 'в пути'}:
            raise SupplierError('Нельзя принять поставку из текущего статуса')
        self.__status = 'получена'

    def cancel(self):
        if self.__status == 'получена':
            raise SupplierError('Нельзя отменить уже полученную поставку')
        self.__status = 'отменена'

    def calculate_delivered_weight(self):
        return sum(batch.quantity_kg for batch in self.batches)

