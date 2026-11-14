"""Исключения предметной области кулинарии."""

from .culinary_exception import CulinaryException
from .invalid_ingredient_exception import InvalidIngredientException
from .insufficient_stock_exception import InsufficientStockException
from .expired_product_exception import ExpiredProductException
from .invalid_recipe_exception import InvalidRecipeException
from .cooking_time_exception import CookingTimeException
from .invalid_temperature_exception import InvalidTemperatureException
from .unavailable_tool_exception import UnavailableToolException
from .invalid_order_exception import InvalidOrderException
from .payment_exception import PaymentException
from .allergen_exception import AllergenException
from .portion_exception import PortionException

# Совместимость с ранее созданными модулями и классами исключений.
from .culinaryerror import CulinaryError
from .invalidingredienterror import InvalidIngredientError
from .insufficientingredienterror import InsufficientIngredientError
from .expiredingredienterror import ExpiredIngredientError
from .recipenotfounderror import RecipeNotFoundError
from .invalidrecipesteperror import InvalidRecipeStepError
from .dishunavailableerror import DishUnavailableError
from .kitchenequipmenterror import KitchenEquipmentError
from .warehousecapacityerror import WarehouseCapacityError
from .suppliererror import SupplierError
from .orderstateerror import OrderStateError
from .paymenterror import PaymentError

__all__ = [
    "CulinaryException",
    "InvalidIngredientException",
    "InsufficientStockException",
    "ExpiredProductException",
    "InvalidRecipeException",
    "CookingTimeException",
    "InvalidTemperatureException",
    "UnavailableToolException",
    "InvalidOrderException",
    "PaymentException",
    "AllergenException",
    "PortionException",
    "CulinaryError",
    "InvalidIngredientError",
    "InsufficientIngredientError",
    "ExpiredIngredientError",
    "RecipeNotFoundError",
    "InvalidRecipeStepError",
    "DishUnavailableError",
    "KitchenEquipmentError",
    "WarehouseCapacityError",
    "SupplierError",
    "OrderStateError",
    "PaymentError",
]
