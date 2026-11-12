"""Помощник кухни."""
from .person import Person
class KitchenAssistant(Person):
    def __init__(self,name,phone,email,age,assigned_area):
        super().__init__(name,phone,email,age); self.__assigned_area=assigned_area
    @property
    def assigned_area(self): return self.__assigned_area
    def change_area(self,area):
        if not str(area).strip(): raise ValueError("Зона работы не может быть пустой")
        self.__assigned_area=area
    def prepare_work_area(self,tools): return all(getattr(tool,"is_clean",False) for tool in tools)
    def count_unclean_tools(self,tools): return sum(not getattr(tool,"is_clean",False) for tool in tools)
