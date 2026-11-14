from culinary.exceptions import (
    InsufficientIngredientError,
    KitchenEquipmentError,
    UnavailableToolException,
)
from culinary.validation import is_number, require_number, require_text
from .cooking_equipment import CookingEquipment
from .workstation import Workstation


class Kitchen:
    """Кухня: проверяет оборудование и списывает ингредиенты при приготовлении."""

    MAX_CLEANLINESS = 100
    MIN_CLEANLINESS_FOR_COOKING = 80

    def __init__(self, name, workstations=None, equipment=None, cleanliness_level=MAX_CLEANLINESS):
        self.__name = require_text(name, "Название кухни не может быть пустым", KitchenEquipmentError)
        if not is_number(cleanliness_level) or not 0 <= cleanliness_level <= self.MAX_CLEANLINESS:
            raise KitchenEquipmentError("Уровень чистоты должен быть от 0 до 100")
        self.__cleanliness_level = cleanliness_level
        self.__workstations = []
        self.__equipment = []
        for workstation in workstations or []:
            self.add_workstation(workstation)
        for item in equipment or []:
            self.register_equipment(item)

    @property
    def name(self):
        return self.__name

    @property
    def workstations(self):
        return tuple(self.__workstations)

    @property
    def equipment(self):
        return tuple(self.__equipment)

    @property
    def cleanliness_level(self):
        return self.__cleanliness_level

    def add_workstation(self, workstation):
        if not isinstance(workstation, Workstation):
            raise TypeError("Ожидается объект Workstation")
        if any(item.number == workstation.number for item in self.__workstations):
            raise KitchenEquipmentError(f"Рабочее место №{workstation.number} уже существует")
        self.__workstations.append(workstation)

    def register_equipment(self, equipment):
        if not isinstance(equipment, CookingEquipment):
            raise TypeError("Ожидается объект CookingEquipment")
        if equipment not in self.__equipment:
            self.__equipment.append(equipment)

    def find_free_workstation(self):
        return next((item for item in self.__workstations if not item.is_occupied), None)

    def is_clean(self, minimum=MIN_CLEANLINESS_FOR_COOKING):
        return self.cleanliness_level >= minimum

    def soil(self, amount):
        require_number(amount, "Загрязнение должно быть положительным", KitchenEquipmentError, positive=True)
        self.__cleanliness_level = max(0, self.__cleanliness_level - amount)

    def record_cleaning(self):
        self.__cleanliness_level = self.MAX_CLEANLINESS

    def check_readiness(self):
        """Кухня чистая, всё оборудование и инструменты пригодны к работе."""
        if not self.is_clean():
            raise KitchenEquipmentError("Кухня не соответствует санитарным нормам")
        for equipment in self.__equipment:
            if not equipment.is_operational():
                raise KitchenEquipmentError(f"Оборудование «{equipment.name}» неисправно")
        for workstation in self.__workstations:
            unusable = workstation.find_unusable_tools()
            if unusable:
                raise UnavailableToolException(f"Инструмент «{unusable[0].name}» недоступен")
        return True

    @staticmethod
    def _use_optional(entry, warehouse, multiplier):
        """Списывает необязательный ингредиент, если он свежий и его хватает; иначе пропускает."""
        ingredient = entry.ingredient
        amount_kg = entry.amount_in_kilograms(multiplier)
        enough = ingredient.weight >= entry.amount_in_grams(multiplier)
        if not ingredient.check_expiration() or not enough:
            return
        try:
            warehouse.deduct_ingredient(ingredient, amount_kg)
        except InsufficientIngredientError:
            return

    def validate_recipe(self, recipe, warehouse, multiplier=1):
        if not is_number(multiplier) or multiplier <= 0:
            raise ValueError("Коэффициент рецепта должен быть положительным")
        self.check_readiness()
        for ingredient, amount_grams, amount_kg in recipe.calculate_requirements(multiplier):
            ingredient.require_fresh()
            self._check_stock(ingredient, amount_grams, amount_kg, warehouse)

    @staticmethod
    def _check_stock(ingredient, amount_grams, amount_kg, warehouse):
        stock_item = warehouse.get_stock_item(ingredient)
        if stock_item is not None and stock_item.ingredient is not ingredient:
            raise InsufficientIngredientError(f"Складская партия «{ingredient.name}» не соответствует рецепту")
        if ingredient.weight < amount_grams:
            raise InsufficientIngredientError(f"Недостаточно «{ingredient.name}» для рецепта")
        if warehouse.get_available_quantity(ingredient) < amount_kg:
            raise InsufficientIngredientError(f"Недостаточно «{ingredient.name}» на складе")

    def cook_recipe(self, recipe, warehouse, multiplier=1):
        self.validate_recipe(recipe, warehouse, multiplier)
        for ingredient, _, amount_kg in recipe.calculate_requirements(multiplier):
            warehouse.deduct_ingredient(ingredient, amount_kg)
        for entry in recipe.ingredients:
            if entry.is_optional:
                self._use_optional(entry, warehouse, multiplier)
        return True
