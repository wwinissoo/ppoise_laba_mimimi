from culinary.exceptions import KitchenEquipmentError
from culinary.validation import require_text


class KitchenTool:
    """Кухонный инвентарь (посуда, ножи и т. п.) с состоянием и чистотой."""

    CONDITIONS = ("новый", "исправен", "изношен", "повреждён")
    USABLE_CONDITIONS = ("новый", "исправен", "изношен")

    def __init__(self, name, material, condition="исправен", is_clean=True):
        self.__name = require_text(name, "Название инструмента обязательно", KitchenEquipmentError)
        self.__material = require_text(material, "Материал инструмента обязателен", KitchenEquipmentError)
        if condition not in self.CONDITIONS:
            raise KitchenEquipmentError(f"Состояние инструмента должно быть одним из: {', '.join(self.CONDITIONS)}")
        self.__condition = condition
        self.__is_clean = bool(is_clean)

    @property
    def name(self):
        return self.__name

    @property
    def material(self):
        return self.__material

    @property
    def condition(self):
        return self.__condition

    @property
    def is_clean(self):
        return self.__is_clean

    def clean(self):
        self.__is_clean = True

    def use(self):
        """Использование инструмента: он становится грязным."""
        if not self.is_usable():
            raise KitchenEquipmentError(f"Инструмент «{self.name}» нельзя использовать")
        self.__is_clean = False

    def mark_damaged(self):
        self.__condition = "повреждён"

    def repair(self):
        if self.__condition != "повреждён":
            return False
        self.__condition = "изношен"
        return True

    def is_usable(self):
        return self.is_clean and self.condition in self.USABLE_CONDITIONS
