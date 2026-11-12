"""Повар без закреплённой специализации."""
from .person import Person
class Cook(Person):
    def __init__(self,name,phone,email,age,shift_hours=8,skill_level="начальный"):
        super().__init__(name,phone,email,age)
        if shift_hours <= 0: raise ValueError("Длительность смены должна быть положительной")
        self.__shift_hours=shift_hours; self.__skill_level=skill_level
    @property
    def shift_hours(self): return self.__shift_hours
    @property
    def skill_level(self): return self.__skill_level
    def estimate_shift_end(self,start_hour): return (start_hour+self.shift_hours)%24
    def improve_skill(self,new_level): self.__skill_level=new_level
