from culinary.validation import require_positive_int
from culinary.exceptions import KitchenEquipmentError
from culinary.people.person import Person
from .kitchen_tool import KitchenTool


class Workstation:
    """Рабочее место кухни с закреплённым сотрудником и набором инструментов."""

    def __init__(self, number, assigned_worker=None, tools=None, is_occupied=False):
        require_positive_int(
            number, "Номер рабочего места должен быть положительным целым числом", KitchenEquipmentError
        )
        self.__number = number
        self.__assigned_worker = None
        self.__is_occupied = False
        self.__tools = []
        for tool in tools or []:
            self.add_tool(tool)
        if assigned_worker is not None:
            self.assign_worker(assigned_worker)
        elif is_occupied:
            raise KitchenEquipmentError("Занятое рабочее место должно иметь сотрудника")

    @property
    def number(self):
        return self.__number

    @property
    def assigned_worker(self):
        return self.__assigned_worker

    @property
    def tools(self):
        return tuple(self.__tools)

    @property
    def is_occupied(self):
        return self.__is_occupied

    def assign_worker(self, worker):
        if not isinstance(worker, Person):
            raise TypeError("За рабочим местом может быть закреплён только сотрудник (Person)")
        if self.__is_occupied and self.__assigned_worker is not worker:
            raise KitchenEquipmentError(f"Рабочее место №{self.number} уже занято")
        self.__assigned_worker = worker
        self.__is_occupied = True

    def release(self):
        self.__assigned_worker = None
        self.__is_occupied = False

    def add_tool(self, tool):
        if not isinstance(tool, KitchenTool):
            raise TypeError("На рабочее место можно добавить только KitchenTool")
        if tool not in self.__tools:
            self.__tools.append(tool)

    def find_unusable_tools(self):
        return [tool for tool in self.__tools if not tool.is_usable()]
