import pytest

from culinary import exceptions
from culinary.exceptions import CulinaryError, CulinaryException

GROUP_EXCEPTIONS = [
    "InvalidIngredientException",
    "InsufficientStockException",
    "ExpiredProductException",
    "InvalidRecipeException",
    "CookingTimeException",
    "InvalidTemperatureException",
    "InvalidOrderException",
    "PaymentException",
    "AllergenException",
    "PortionException",
]

ERRORS_WITH_DEFAULT_MESSAGE = {
    "CulinaryError": "Ошибка кулинарной системы",
    "InvalidIngredientError": "Некорректные данные ингредиента",
    "InsufficientIngredientError": "Недостаточно ингредиента",
    "ExpiredIngredientError": "Срок годности ингредиента истёк",
    "RecipeNotFoundError": "Рецепт не найден",
    "InvalidRecipeStepError": "Некорректный шаг рецепта",
    "DishUnavailableError": "Блюдо недоступно",
    "KitchenEquipmentError": "Ошибка кухонного оборудования",
    "WarehouseCapacityError": "Превышена вместимость склада",
    "SupplierError": "Ошибка поставщика",
    "OrderStateError": "Недопустимое состояние заказа",
    "PaymentError": "Ошибка оплаты",
}

PAIRED = {
    "InvalidIngredientError": "InvalidIngredientException",
    "InsufficientIngredientError": "InsufficientStockException",
    "ExpiredIngredientError": "ExpiredProductException",
    "InvalidRecipeStepError": "InvalidRecipeException",
    "PaymentError": "PaymentException",
}


def test_exports_all_24_exceptions():
    assert len(exceptions.__all__) == 24
    assert all(issubclass(getattr(exceptions, name), CulinaryException) for name in exceptions.__all__)


@pytest.mark.parametrize("name", GROUP_EXCEPTIONS)
def test_group_exception_carries_message(name):
    error_class = getattr(exceptions, name)
    with pytest.raises(CulinaryException, match="сообщение"):
        raise error_class("сообщение")


@pytest.mark.parametrize("name, message", ERRORS_WITH_DEFAULT_MESSAGE.items())
def test_error_default_message(name, message):
    error_class = getattr(exceptions, name)
    assert str(error_class()) == message and str(error_class("своё")) == "своё"
    assert issubclass(error_class, CulinaryError)


@pytest.mark.parametrize("error_name, group_name", PAIRED.items())
def test_errors_belong_to_their_group(error_name, group_name):
    assert issubclass(getattr(exceptions, error_name), getattr(exceptions, group_name))


def test_unavailable_tool_is_equipment_error():
    assert issubclass(exceptions.UnavailableToolException, exceptions.KitchenEquipmentError)
    assert str(exceptions.UnavailableToolException()) == "Ошибка кухонного оборудования"
