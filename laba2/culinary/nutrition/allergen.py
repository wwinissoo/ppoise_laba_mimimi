"""Аллерген и правила его проверки в составе рецепта."""
class Allergen:
    def __init__(self,name,severity="обычная",description=""):
        if not str(name).strip(): raise ValueError("Название аллергена не может быть пустым")
        self.__name=str(name).strip(); self.__severity=severity; self.__description=description
    @property
    def name(self): return self.__name
    @property
    def severity(self): return self.__severity
    @property
    def description(self): return self.__description
    def matches_ingredient(self,ingredient):
        ingredient_name=getattr(ingredient,"name",str(ingredient)).casefold()
        return self.name.casefold() in ingredient_name
    def describe(self): return f"{self.name}: {self.severity}. {self.description}".strip()
