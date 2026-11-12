from culinary.ingredients.ingredient import Ingredient
from culinary.exceptions import InvalidIngredientError

class Flour(Ingredient):
    """Класс Flour предметной области «Кулинария»."""
    PERCENT_MIN = 0
    PERCENT_MAX = 100
    """Модель ингредиента типа Flour."""
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 protein_percentage=10, gluten_content="среднее", flour_type="пшеничная"):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if not self.PERCENT_MIN <= protein_percentage <= self.PERCENT_MAX:
            raise InvalidIngredientError("Белок должен быть от 0 до 100")
        self.__protein_percentage = protein_percentage
        self.__gluten_content = gluten_content
        self.__flour_type = flour_type
        self.__is_sifted = False

    @property
    def protein_percentage(self): return self.__protein_percentage
    @property
    def gluten_content(self): return self.__gluten_content
    @property
    def flour_type(self): return self.__flour_type
    @property
    def is_sifted(self): return self.__is_sifted

    def sift(self):
        self.__is_sifted = True
        return self.weight

    def calculate_protein_weight(self):
        return self.weight * self.__protein_percentage / 100

    def is_suitable_for_bread(self):
        return self.__gluten_content in ("среднее", "высокое")

    def change_flour_type(self, flour_type):
        if not isinstance(flour_type, str) or not flour_type.strip():
            raise InvalidIngredientError("Тип муки не может быть пустым")
        self.__flour_type = flour_type.strip()
