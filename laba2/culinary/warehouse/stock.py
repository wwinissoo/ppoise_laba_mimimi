"""Складской запас."""
class Stock:
    def __init__(self): self.__items={}
    @property
    def items(self): return tuple(self.__items.values())
    def add_item(self,stock_item): self.__items[stock_item.ingredient.name.casefold()]=stock_item
    def get_item(self,ingredient_name): return self.__items.get(ingredient_name.casefold())
    def total_quantity(self): return sum(item.quantity_kg for item in self.__items.values())
    def below_minimum(self): return [item for item in self.__items.values() if item.quantity_kg < item.minimum_kg]
