"""Фасад предметной области: связывает склад, кухню, рецепты, меню и заказы в памяти."""

from datetime import datetime

from culinary.dishes.menu_item import MenuItem
from culinary.exceptions import (
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
from culinary.ingredients.ingredient import Ingredient
from culinary.kitchen.kitchen import Kitchen
from culinary.orders.delivery import Delivery
from culinary.orders.order import Order
from culinary.orders.order_item import OrderItem
from culinary.orders.payment import Payment
from culinary.people.customer import Customer
from culinary.recipes.recipe_manager import RecipeManager
from culinary.warehouse.purchase import Purchase
from culinary.warehouse.stock_item import StockItem
from culinary.warehouse.warehouse import Warehouse

GRAMS_PER_KILOGRAM = Ingredient.GRAMS_PER_KILOGRAM
DEFAULT_LOCATION_CODE = "A-1"
SUPPLY_LOCATION_CODE = "Поставка"


class CulinarySystem:
    """Сервис приложения; все репозитории — обычные коллекции в памяти."""

    def __init__(self, warehouse, kitchen):
        if not isinstance(warehouse, Warehouse):
            raise TypeError("Ожидается объект Warehouse")
        if not isinstance(kitchen, Kitchen):
            raise TypeError("Ожидается объект Kitchen")
        self.__warehouse = warehouse
        self.__kitchen = kitchen
        self.__recipe_manager = RecipeManager()
        self.__menu_items = {}
        self.__orders = {}
        self.__order_payments = {}
        self.__delivery_payments = {}
        self.__deliveries = {}
        self.__purchase_payments = {}
        self.__ingredients = {}

    @property
    def warehouse(self):
        return self.__warehouse

    @property
    def kitchen(self):
        return self.__kitchen

    @property
    def recipe_manager(self):
        return self.__recipe_manager

    @property
    def menu_items(self):
        return tuple(self.__menu_items.values())

    @property
    def orders(self):
        return tuple(self.__orders.values())

    @property
    def deliveries(self):
        return tuple(self.__deliveries.values())

    @staticmethod
    def _key(name):
        return name.strip().casefold()

    def _require_free_capacity(self, quantity_kg):
        if not self.warehouse.has_free_capacity(quantity_kg):
            raise WarehouseCapacityError("Недостаточно места на складе")

    def register_ingredient(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("Ожидается объект Ingredient")
        existing = self.__ingredients.get(self._key(ingredient.name))
        if existing is not None and existing is not ingredient:
            raise SupplierError(f"Ингредиент «{ingredient.name}» уже зарегистрирован")
        stock_item = self.warehouse.get_stock_item(ingredient)
        if stock_item is not None and stock_item.ingredient is not ingredient:
            raise SupplierError(f"Ингредиент «{ingredient.name}» уже зарегистрирован на складе")
        self.__ingredients[self._key(ingredient.name)] = ingredient
        return ingredient

    def add_ingredient(self, ingredient, minimum_kg=0, location_code=DEFAULT_LOCATION_CODE):
        self.register_ingredient(ingredient)
        if self.warehouse.get_stock_item(ingredient) is not None:
            raise ValueError("Ингредиент уже зарегистрирован на складе")
        quantity_kg = ingredient.weight / GRAMS_PER_KILOGRAM
        stock_item = StockItem(ingredient, quantity_kg, minimum_kg, location_code)
        self.warehouse.add_stock_item(stock_item)
        return stock_item

    def get_ingredient(self, name):
        if not isinstance(name, str):
            raise TypeError("Название ингредиента должно быть строкой")
        ingredient = self.__ingredients.get(self._key(name))
        if ingredient is not None:
            return ingredient
        stock_item = self.warehouse.get_stock_item(name)
        return None if stock_item is None else self.register_ingredient(stock_item.ingredient)

    def _put_on_stock(self, ingredient, quantity_kg, location_code):
        """Принимает поступление: создаёт складскую позицию или пополняет существующую."""
        self._require_free_capacity(quantity_kg)
        stock_item = self.warehouse.get_stock_item(ingredient)
        incoming_grams = quantity_kg * GRAMS_PER_KILOGRAM
        if stock_item is not None:
            ingredient.receive(incoming_grams)
            stock_item.receive(quantity_kg)
            return stock_item
        if ingredient.weight == 0:
            ingredient.receive(incoming_grams)
        elif ingredient.weight != incoming_grams:
            raise SupplierError("Вес партии ингредиента должен совпадать с поступлением на склад")
        return self.add_ingredient(ingredient, location_code=location_code)

    def restock_ingredient(self, ingredient, quantity_kg):
        if quantity_kg <= 0:
            raise ValueError("Количество поступления должно быть положительным")
        self.register_ingredient(ingredient)
        return self._put_on_stock(ingredient, quantity_kg, DEFAULT_LOCATION_CODE)

    def delete_ingredient(self, ingredient_name):
        return self.warehouse.remove_stock_item(ingredient_name)

    def add_recipe(self, recipe):
        self.recipe_manager.add_recipe(recipe)
        return recipe

    def _menu_items_using(self, recipe):
        return [item for item in self.__menu_items.values() if item.dish.recipe is recipe]

    def update_recipe(self, name, recipe):
        old_recipe = self.recipe_manager.find_recipe(name)
        updated = self.recipe_manager.update_recipe(name, recipe)
        for item in self._menu_items_using(old_recipe):
            item.dish.replace_recipe(updated)
        return updated

    def delete_recipe(self, name):
        try:
            recipe = self.recipe_manager.find_recipe(name)
        except RecipeNotFoundError:
            return False
        used_by = self._menu_items_using(recipe)
        if used_by:
            raise InvalidRecipeException(f"Рецепт используется в меню блюдом «{used_by[0].dish.name}»")
        return self.recipe_manager.remove_recipe(name)

    def add_menu_item(self, item):
        if not isinstance(item, MenuItem):
            raise TypeError("Ожидается объект MenuItem")
        key = self._key(item.dish.name)
        if key in self.__menu_items:
            raise DishUnavailableError(f"Блюдо «{item.dish.name}» уже есть в меню")
        self.__menu_items[key] = item
        return item

    def set_dish_availability(self, dish_name, available):
        item = self._find_menu_item(dish_name)
        if available:
            item.mark_available()
        else:
            item.mark_unavailable()
        return item

    def _find_menu_item(self, dish_name):
        item = self.__menu_items.get(self._key(dish_name))
        if item is None:
            raise DishUnavailableError(f"Блюдо «{dish_name}» отсутствует в меню")
        return item

    def create_order_item(self, dish_name, quantity, note=""):
        menu_item = self._find_menu_item(dish_name)
        menu_item.require_available()
        return OrderItem(menu_item.dish, quantity, menu_item.price, note)

    def _validate_order_item(self, customer, item):
        if not isinstance(item, OrderItem):
            raise TypeError("Позиции заказа должны быть объектами OrderItem")
        menu_item = self._find_menu_item(item.dish.name)
        menu_item.require_available()
        if item.dish is not menu_item.dish or item.unit_price != menu_item.price:
            raise InvalidOrderException("Блюдо и цена позиции должны совпадать с действующим меню")
        customer.ensure_can_eat(item.dish)

    def _validate_order_items(self, customer, items):
        items = list(items)
        if not items:
            raise InvalidOrderException("Заказ должен содержать хотя бы одно блюдо")
        for item in items:
            self._validate_order_item(customer, item)
        return items

    def create_order(self, order_number, customer, items, created_at=None):
        if order_number in self.__orders:
            raise InvalidOrderException(f"Заказ «{order_number}» уже существует")
        if not isinstance(customer, Customer):
            raise TypeError("Ожидается объект Customer")
        items = self._validate_order_items(customer, items)
        order = Order(order_number, customer, items, Order.NEW, created_at or datetime.now())
        self.__orders[order_number] = order
        return order

    def get_order(self, order_number):
        try:
            return self.__orders[order_number]
        except KeyError as error:
            raise InvalidOrderException(f"Заказ «{order_number}» не найден") from error

    def _is_order_paid(self, order_number):
        payment = self.__order_payments.get(order_number)
        return payment is not None and payment.is_paid()

    def edit_order(self, order_number, items):
        order = self.get_order(order_number)
        if self._is_order_paid(order_number):
            raise OrderStateError("Оплаченный заказ нельзя редактировать")
        order.replace_items(self._validate_order_items(order.customer, items))
        return order

    @staticmethod
    def _require_no_active_payment(payments, key, message):
        existing = payments.get(key)
        if existing is not None and not existing.is_refunded():
            raise PaymentError(message)

    def pay_order(self, order_number, amount, method):
        order = self.get_order(order_number)
        if order.status != Order.NEW:
            raise OrderStateError("Оплатить можно только новый заказ")
        self._require_no_active_payment(self.__order_payments, order_number, "Для заказа уже зарегистрирован платеж")
        payment = Payment(order, amount, method, purpose=Payment.FOR_ORDER)
        payment.process()
        self.__order_payments[order_number] = payment
        return payment

    def refund_order(self, order_number):
        order = self.get_order(order_number)
        payment = self.__order_payments.get(order_number)
        if order.status != Order.NEW or payment is None:
            raise OrderStateError("Возврат возможен только для нового оплаченного заказа")
        return payment.refund()

    def cancel_order(self, order_number):
        order = self.get_order(order_number)
        if self._is_order_paid(order_number):
            raise OrderStateError("Перед отменой оплаченного заказа оформите возврат")
        order.change_status(Order.CANCELLED)
        return order

    def pay_purchase(self, purchase, amount, method):
        if not isinstance(purchase, Purchase):
            raise TypeError("Ожидается объект Purchase")
        if purchase.status != Purchase.AWAITING_PAYMENT:
            raise OrderStateError("Закупка не ожидает оплаты")
        payment = Payment(purchase, amount, method, purpose=Payment.FOR_PURCHASE)
        payment.process()
        purchase.mark_paid()
        self.__purchase_payments[id(purchase)] = payment
        return payment

    def receive_purchase(self, purchase):
        payment = self.__purchase_payments.get(id(purchase))
        if payment is None or not payment.is_paid():
            raise PaymentError("Нельзя принять неоплаченную закупку")
        self.register_ingredient(purchase.ingredient)
        purchase.ingredient.require_fresh()
        stock_item = self._put_on_stock(purchase.ingredient, purchase.quantity_kg, SUPPLY_LOCATION_CODE)
        purchase.mark_received()
        return stock_item

    def _find_delivery(self, order_number):
        delivery = self.__deliveries.get(order_number)
        if delivery is None:
            raise InvalidOrderException("Для заказа не оформлена доставка")
        return delivery

    def pay_delivery(self, order_number, amount, method):
        order = self.get_order(order_number)
        delivery = self._find_delivery(order_number)
        if delivery.is_cancelled():
            raise OrderStateError("Нельзя оплатить отменённую доставку")
        self._require_no_active_payment(self.__delivery_payments, order_number, "Доставка уже оплачена")
        payment = Payment(order, amount, method, purpose=Payment.FOR_DELIVERY, expected_amount=delivery.delivery_fee)
        payment.process()
        self.__delivery_payments[order_number] = payment
        return payment

    def _collect_requirements(self, order):
        """Суммарная потребность заказа: id ингредиента → (ингредиент, граммы, килограммы)."""
        required = {}
        for order_item in order.items:
            self._find_menu_item(order_item.dish.name).require_available()
            multiplier = order_item.quantity / order_item.dish.portions
            recipe = order_item.dish.recipe
            self.kitchen.validate_recipe(recipe, self.warehouse, multiplier)
            for ingredient, grams, kilograms in recipe.calculate_requirements(multiplier):
                _, total_grams, total_kg = required.get(id(ingredient), (ingredient, 0, 0))
                required[id(ingredient)] = (ingredient, total_grams + grams, total_kg + kilograms)
        return required

    def _check_total_stock(self, required):
        for ingredient, grams, kilograms in required.values():
            available_kg = self.warehouse.get_available_quantity(ingredient)
            if ingredient.weight < grams or available_kg < kilograms:
                raise InsufficientIngredientError(f"Недостаточно «{ingredient.name}» для всего заказа")

    def cook_order(self, order_number):
        order = self.get_order(order_number)
        if order.status != Order.NEW:
            raise OrderStateError("Приготовить можно только новый заказ")
        if not self._is_order_paid(order_number):
            raise PaymentError("Для приготовления заказ должен быть оплачен")
        self._check_total_stock(self._collect_requirements(order))
        order.change_status(Order.COOKING)
        for order_item in order.items:
            multiplier = order_item.quantity / order_item.dish.portions
            self.kitchen.cook_recipe(order_item.dish.recipe, self.warehouse, multiplier)
        order.change_status(Order.READY)
        return order

    def hand_over_order(self, order_number):
        """Выдача готового заказа на месте (самовывоз)."""
        order = self.get_order(order_number)
        delivery = self.__deliveries.get(order_number)
        if delivery is not None and not delivery.is_cancelled():
            raise OrderStateError("Заказ оформлен на доставку; выдача — через курьера")
        if order.status != Order.READY:
            raise OrderStateError("Выдать можно только готовый заказ")
        order.change_status(Order.HANDED_OVER)
        return order

    def create_delivery(self, order_number, address, delivery_fee=0):
        order = self.get_order(order_number)
        if order.status != Order.READY:
            raise OrderStateError("Доставку можно оформить только для готового заказа")
        if order_number in self.__deliveries:
            raise OrderStateError("Для заказа доставка уже оформлена")
        delivery = Delivery(order, address, delivery_fee)
        self.__deliveries[order_number] = delivery
        return delivery

    def update_delivery_status(self, order_number, status):
        delivery = self._find_delivery(order_number)
        payment = self.__delivery_payments.get(order_number)
        fee_unpaid = delivery.delivery_fee > 0 and (payment is None or not payment.is_paid())
        if status == Delivery.IN_TRANSIT and fee_unpaid:
            raise PaymentError("Перед отправкой нужно оплатить доставку")
        delivery.update_status(status)
        if delivery.is_completed():
            delivery.order.change_status(Order.HANDED_OVER)
        return delivery
