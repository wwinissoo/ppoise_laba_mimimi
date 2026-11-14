"""Аллерген и правила его проверки в составе рецепта."""

from culinary.exceptions import AllergenException
from culinary.validation import require_text


class Allergen:
    SEVERITIES = ("лёгкая", "обычная", "тяжёлая")

    def __init__(self, name, severity="обычная", description=""):
        self.__name = require_text(name, "Название аллергена не может быть пустым")
        if severity not in self.SEVERITIES:
            raise ValueError(f"Степень опасности должна быть одной из: {', '.join(self.SEVERITIES)}")
        self.__severity = severity
        self.__description = str(description or "").strip()

    @property
    def name(self):
        return self.__name

    @property
    def severity(self):
        return self.__severity

    @property
    def description(self):
        return self.__description

    def matches_ingredient(self, ingredient):
        ingredient_name = getattr(ingredient, "name", str(ingredient)).casefold()
        return self.name.casefold() in ingredient_name

    def find_in_recipe(self, recipe):
        return [item.ingredient for item in recipe.ingredients if self.matches_ingredient(item.ingredient)]

    def ensure_absent(self, recipe):
        """Вызывает AllergenException, если аллерген входит в рецепт."""
        found = self.find_in_recipe(recipe)
        if found:
            raise AllergenException(f"Рецепт «{recipe.name}» содержит аллерген «{self.name}» ({found[0].name})")
        return True

    def describe(self):
        return f"{self.name}: {self.severity}. {self.description}".strip()
