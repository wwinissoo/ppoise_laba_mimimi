import pytest

from culinary.application import CulinarySystem
from culinary.exceptions import (
    AllergenException,
    DishUnavailableError,
    InsufficientIngredientError,
    InvalidOrderException,
    InvalidRecipeException,
    OrderStateError,
    PaymentError,
    RecipeNotFoundError,
    SupplierError,
    WarehouseCapacityError,
)
from culinary.ingredients import Ingredient, Vegetable
from culinary.kitchen import Kitchen
from culinary.nutrition import Allergen
from culinary.people import Customer
from culinary.recipes import Recipe
from culinary.warehouse import Purchase, Supplier, Warehouse


def new_onion():
    return Ingredient("Лук", 0, 50, 40, 10, 4, allow_zero=True)


def place_paid_order(system, customer, number="ORD-1", portions=2):
    system.create_order(number, customer, [system.create_order_item("Салат", portions)])
    system.pay_order(number, 150 * portions, "карта")


class TestCulinarySystem:
    def test_requires_warehouse_and_kitchen(self):
        with pytest.raises(TypeError):
            CulinarySystem("склад", Kitchen("Кухня"))
        with pytest.raises(TypeError):
            CulinarySystem(Warehouse("Склад", ""), "кухня")

    def test_properties(self, system):
        assert system.kitchen.name == "Кухня" and system.orders == () and system.deliveries == ()
        assert len(system.menu_items) == 1 and system.recipe_manager.recipes


class TestIngredients:
    def test_register_and_find(self, system, tomato):
        onion = new_onion()
        assert system.register_ingredient(onion) is onion and system.get_ingredient(" лук ") is onion
        assert system.get_ingredient("Помидор") is tomato and system.get_ingredient("Чеснок") is None
        with pytest.raises(TypeError):
            system.get_ingredient(5)
        with pytest.raises(TypeError):
            system.register_ingredient("лук")

    def test_conflicting_objects(self, system):
        system.register_ingredient(new_onion())
        with pytest.raises(SupplierError):
            system.register_ingredient(new_onion())
        with pytest.raises(SupplierError):
            system.register_ingredient(Vegetable("Помидор", 1000, 200, 18, 7, 4))

    def test_found_in_stock_is_cached(self, tomato):
        warehouse = Warehouse("Склад", "")
        system = CulinarySystem(warehouse, Kitchen("Кухня"))
        system.add_ingredient(tomato)
        assert system.get_ingredient("помидор") is tomato

    def test_add_duplicate_stock(self, system, tomato):
        with pytest.raises(ValueError):
            system.add_ingredient(tomato)

    def test_restock(self, system, tomato):
        assert system.restock_ingredient(tomato, 1).quantity_kg == 2 and tomato.weight == 2000
        onion = new_onion()
        assert system.restock_ingredient(onion, 3).quantity_kg == 3 and onion.weight == 3000
        with pytest.raises(ValueError):
            system.restock_ingredient(tomato, 0)
        with pytest.raises(SupplierError):
            system.restock_ingredient(Vegetable("Чеснок", 500, 300, 150, 30, 4), 2)
        with pytest.raises(WarehouseCapacityError):
            system.restock_ingredient(tomato, 1000)

    def test_restock_with_matching_batch(self, system):
        garlic = Vegetable("Чеснок", 2000, 300, 150, 30, 4)
        assert system.restock_ingredient(garlic, 2).quantity_kg == 2

    def test_delete(self, system):
        system.restock_ingredient(new_onion(), 1)
        system.warehouse.deduct_ingredient(system.get_ingredient("Лук"), 1)
        assert system.delete_ingredient("Лук") and not system.delete_ingredient("Лук")


class TestRecipesAndMenu:
    def test_update_propagates_to_menu(self, system, recipe):
        updated = Recipe("Салат", "Новая версия", 5, 2)
        updated.add_ingredient(recipe.ingredients[0].ingredient, 100)
        assert system.update_recipe("Салат", updated) is updated
        assert system.menu_items[0].dish.recipe is updated

    def test_delete_rules(self, system):
        with pytest.raises(InvalidRecipeException):
            system.delete_recipe("Салат")
        assert not system.delete_recipe("Суп")
        system.add_recipe(Recipe("Суп", "", 10, 1))
        assert system.delete_recipe("Суп")
        with pytest.raises(RecipeNotFoundError):
            system.update_recipe("Суп", Recipe("Суп", "", 10, 1))

    def test_menu(self, system):
        with pytest.raises(DishUnavailableError):
            system.add_menu_item(system.menu_items[0])
        with pytest.raises(TypeError):
            system.add_menu_item("салат")
        system.set_dish_availability("салат", False)
        with pytest.raises(DishUnavailableError):
            system.create_order_item("Салат", 1)
        system.set_dish_availability("Салат", True)
        assert system.create_order_item("Салат", 1).unit_price == 150
        with pytest.raises(DishUnavailableError):
            system.create_order_item("Борщ", 1)


class TestOrders:
    def test_create_and_edit(self, system, customer):
        order = system.create_order("ORD-1", customer, [system.create_order_item("Салат", 1)])
        assert system.get_order("ORD-1") is order and system.orders == (order,)
        system.edit_order("ORD-1", [system.create_order_item("Салат", 3)])
        assert order.calculate_total() == 450
        with pytest.raises(InvalidOrderException):
            system.create_order("ORD-1", customer, [system.create_order_item("Салат", 1)])
        with pytest.raises(InvalidOrderException):
            system.get_order("ORD-404")

    def test_validation(self, system, customer, dish):
        from culinary.orders import OrderItem

        with pytest.raises(TypeError):
            system.create_order("ORD-1", "Анна", [system.create_order_item("Салат", 1)])
        with pytest.raises(InvalidOrderException):
            system.create_order("ORD-1", customer, [])
        with pytest.raises(TypeError):
            system.create_order("ORD-1", customer, ["салат"])
        with pytest.raises(InvalidOrderException):
            system.create_order("ORD-1", customer, [OrderItem(dish, 1, 1)])

    def test_allergies_are_checked(self, system):
        allergic = Customer("Борис", "+7 900 555-55-55", "", 30, allergies=[Allergen("помидор")])
        with pytest.raises(AllergenException):
            system.create_order("ORD-9", allergic, [system.create_order_item("Салат", 1)])

    def test_payment_rules(self, system, customer):
        place_paid_order(system, customer)
        with pytest.raises(PaymentError):
            system.pay_order("ORD-1", 300, "карта")
        with pytest.raises(OrderStateError):
            system.edit_order("ORD-1", [system.create_order_item("Салат", 1)])
        with pytest.raises(OrderStateError):
            system.cancel_order("ORD-1")
        assert system.refund_order("ORD-1") == 300
        system.pay_order("ORD-1", 300, "карта")
        system.refund_order("ORD-1")
        system.cancel_order("ORD-1")
        with pytest.raises(OrderStateError):
            system.pay_order("ORD-1", 300, "карта")
        with pytest.raises(OrderStateError):
            system.refund_order("ORD-1")


class TestCooking:
    def test_cook_and_hand_over(self, system, customer, tomato):
        place_paid_order(system, customer)
        order = system.cook_order("ORD-1")
        assert order.status == "готов" and tomato.weight == 800
        assert system.hand_over_order("ORD-1").status == "выдан"
        with pytest.raises(OrderStateError):
            system.cook_order("ORD-1")
        with pytest.raises(OrderStateError):
            system.hand_over_order("ORD-1")

    def test_requires_payment(self, system, customer):
        system.create_order("ORD-1", customer, [system.create_order_item("Салат", 1)])
        with pytest.raises(PaymentError):
            system.cook_order("ORD-1")

    def test_checks_total_stock_before_deduction(self, system, customer, tomato):
        items = [system.create_order_item("Салат", 6), system.create_order_item("Салат", 6)]
        system.create_order("ORD-1", customer, items)
        system.pay_order("ORD-1", 1800, "карта")
        with pytest.raises(InsufficientIngredientError):
            system.cook_order("ORD-1")
        assert system.get_order("ORD-1").status == "новый" and tomato.weight == 1000


class TestDelivery:
    def test_full_flow(self, system, customer):
        place_paid_order(system, customer)
        with pytest.raises(OrderStateError):
            system.create_delivery("ORD-1", "ул. Мира, 5")
        order = system.cook_order("ORD-1")
        delivery = system.create_delivery("ORD-1", "ул. Мира, 5", 100)
        assert system.deliveries == (delivery,)
        with pytest.raises(OrderStateError):
            system.create_delivery("ORD-1", "ул. Мира, 5")
        with pytest.raises(OrderStateError):
            system.hand_over_order("ORD-1")
        with pytest.raises(PaymentError):
            system.update_delivery_status("ORD-1", "в пути")
        system.pay_delivery("ORD-1", 100, "онлайн")
        with pytest.raises(PaymentError):
            system.pay_delivery("ORD-1", 100, "онлайн")
        for status in ("готовится", "в пути", "доставлен"):
            system.update_delivery_status("ORD-1", status)
        assert order.status == "выдан"

    def test_cancelled_delivery(self, system, customer):
        place_paid_order(system, customer)
        system.cook_order("ORD-1")
        with pytest.raises(InvalidOrderException):
            system.pay_delivery("ORD-1", 0, "карта")
        with pytest.raises(InvalidOrderException):
            system.update_delivery_status("ORD-1", "отменён")
        system.create_delivery("ORD-1", "ул. Мира, 5")
        system.update_delivery_status("ORD-1", "отменён")
        with pytest.raises(OrderStateError):
            system.pay_delivery("ORD-1", 0, "карта")
        assert system.hand_over_order("ORD-1").status == "выдан"


class TestPurchases:
    def test_pay_and_receive(self, system, tomato):
        purchase = Purchase(Supplier("Ферма", "+7 900", [tomato]), tomato, 2, 180)
        with pytest.raises(PaymentError):
            system.receive_purchase(purchase)
        system.pay_purchase(purchase, 360, "карта")
        with pytest.raises(OrderStateError):
            system.pay_purchase(purchase, 360, "карта")
        assert system.receive_purchase(purchase).quantity_kg == pytest.approx(3) and purchase.received
        with pytest.raises(TypeError):
            system.pay_purchase("закупка", 1, "карта")

    def test_new_ingredient_batch(self, system):
        garlic = Vegetable("Чеснок", 2000, 300, 150, 30, 4)
        purchase = Purchase(Supplier("Ферма", "+7 900", [garlic]), garlic, 2, 300)
        system.pay_purchase(purchase, 600, "карта")
        stock_item = system.receive_purchase(purchase)
        assert stock_item.location_code == "Поставка" and stock_item.quantity_kg == 2
