"""Инвентарная ведомость кухонного оборудования."""
class KitchenInventory:
    def __init__(self): self.__tools=[]; self.__equipment=[]
    @property
    def tools(self): return tuple(self.__tools)
    @property
    def equipment(self): return tuple(self.__equipment)
    def register_tool(self,tool): self.__tools.append(tool)
    def register_equipment(self,equipment): self.__equipment.append(equipment)
    def count_items(self): return len(self.__tools)+len(self.__equipment)
    def find_unavailable(self):
        return [item for item in self.__equipment if getattr(item,"status","") not in ("включено","выключено","готово")]+[item for item in self.__tools if getattr(item,"condition","") not in ("исправна","хорошее","новое")]
