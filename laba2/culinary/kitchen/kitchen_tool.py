class KitchenTool:
    """Объект предметной области: KitchenTool."""

    def __init__(self, name, material, condition, is_clean):
        self.__name = name
        self.__material = material
        self.__condition = condition
        self.__is_clean = is_clean

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

    def mark_damaged(self):
        self.__condition = 'повреждён'

    def is_usable(self):
        return self.is_clean and self.condition == 'исправен'

