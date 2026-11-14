"""Помощник кухни."""

from culinary.validation import require_text
from .person import Person


class KitchenAssistant(Person):
    def __init__(self, name, phone, email, age, assigned_area):
        super().__init__(name, phone, email, age)
        self.__assigned_area = require_text(assigned_area, "Зона работы не может быть пустой")

    @property
    def assigned_area(self):
        return self.__assigned_area

    def change_area(self, area):
        self.__assigned_area = require_text(area, "Зона работы не может быть пустой")

    def prepare_work_area(self, tools):
        """Моет все грязные инструменты зоны; возвращает количество вымытых."""
        dirty = [tool for tool in tools if not tool.is_clean]
        for tool in dirty:
            tool.clean()
        return len(dirty)

    def count_unclean_tools(self, tools):
        return sum(not tool.is_clean for tool in tools)
