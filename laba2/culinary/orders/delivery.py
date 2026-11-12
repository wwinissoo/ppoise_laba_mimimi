"""Доставка клиентского заказа."""
class Delivery:
    def __init__(self,order,address,delivery_fee=0,status="ожидает"):
        if not str(address).strip() or delivery_fee < 0: raise ValueError("Некорректные данные доставки")
        self.__order=order; self.__address=address; self.__delivery_fee=delivery_fee; self.__status=status
    @property
    def order(self): return self.__order
    @property
    def address(self): return self.__address
    @property
    def delivery_fee(self): return self.__delivery_fee
    @property
    def status(self): return self.__status
    def calculate_total(self): return self.order.calculate_total()+self.delivery_fee
    def update_status(self,status):
        allowed={"ожидает","готовится","в пути","доставлен","отменён"}
        if status not in allowed: raise ValueError("Неизвестный статус доставки")
        self.__status=status
    def is_completed(self): return self.status=="доставлен"
