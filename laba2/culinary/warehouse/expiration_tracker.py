"""Отслеживание сроков годности складских ингредиентов."""
class ExpirationTracker:
    def __init__(self,ingredients=None): self.__ingredients=list(ingredients or [])
    @property
    def ingredients(self): return tuple(self.__ingredients)
    def register(self,ingredient): self.__ingredients.append(ingredient)
    def advance_day(self):
        for ingredient in self.__ingredients: ingredient.pass_day()
    def expired_items(self): return [item for item in self.__ingredients if not item.check_expiration()]
    def fresh_items(self): return [item for item in self.__ingredients if item.check_expiration()]
