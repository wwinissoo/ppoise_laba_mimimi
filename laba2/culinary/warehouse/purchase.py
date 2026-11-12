"""Закупка ингредиентов у поставщика."""
class Purchase:
    def __init__(self,supplier,ingredient,quantity_kg,unit_price):
        if quantity_kg <= 0 or unit_price < 0: raise ValueError("Некорректные параметры закупки")
        self.__supplier=supplier; self.__ingredient=ingredient; self.__quantity_kg=quantity_kg; self.__unit_price=unit_price; self.__received=False
    @property
    def supplier(self): return self.__supplier
    @property
    def ingredient(self): return self.__ingredient
    @property
    def quantity_kg(self): return self.__quantity_kg
    @property
    def unit_price(self): return self.__unit_price
    @property
    def received(self): return self.__received
    def calculate_total(self): return self.quantity_kg*self.unit_price
    def mark_received(self):
        if self.__received: raise ValueError("Закупка уже получена")
        self.__received=True
