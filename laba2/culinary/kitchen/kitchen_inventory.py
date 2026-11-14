"""Инвентарная ведомость кухонного оборудования."""

from .cooking_equipment import CookingEquipment
from .kitchen_tool import KitchenTool


class KitchenInventory:
    def __init__(self):
        self.__tools = []
        self.__equipment = []

    @property
    def tools(self):
        return tuple(self.__tools)

    @property
    def equipment(self):
        return tuple(self.__equipment)

    def register_tool(self, tool):
        if not isinstance(tool, KitchenTool):
            raise TypeError("Ожидается объект KitchenTool")
        if tool not in self.__tools:
            self.__tools.append(tool)

    def register_equipment(self, equipment):
        if not isinstance(equipment, CookingEquipment):
            raise TypeError("Ожидается объект CookingEquipment")
        if equipment not in self.__equipment:
            self.__equipment.append(equipment)

    def count_items(self):
        return len(self.__tools) + len(self.__equipment)

    def find_unavailable(self):
        return [item for item in self.__equipment if not item.is_operational()] + [
            item for item in self.__tools if not item.is_usable()
        ]

    def find_needing_service(self, interval):
        return [item for item in self.__equipment if item.needs_service(interval)]
