"""Интерактивное меню: только ввод/вывод, вся логика — в CulinarySystem."""

from culinary.application import CulinarySystem
from culinary.dishes.dish import Dish
from culinary.dishes.menu_item import MenuItem
from culinary.exceptions import CulinaryException
from culinary.ingredients.ingredient import Ingredient
from culinary.kitchen.kitchen import Kitchen
from culinary.orders.delivery import Delivery
from culinary.orders.payment import Payment
from culinary.people.customer import Customer
from culinary.recipes.recipe import Recipe
from culinary.recipes.recipe_step import RecipeStep
from culinary.warehouse.inventory_manager import InventoryManager
from culinary.warehouse.purchase import Purchase
from culinary.warehouse.supplier import Supplier
from culinary.warehouse.warehouse import Warehouse

WAREHOUSE_NAME = "Основной склад"
WAREHOUSE_LOCATION = "Кухня"
WAREHOUSE_CAPACITY_KG = 10000
KITCHEN_NAME = "Основная кухня"
DEFAULT_DISH_TEMPERATURE = 60
DEFAULT_CATEGORY = "основное"
DEFAULT_UNIT = "г"
DEFAULT_PAYMENT_METHOD = "карта"
FIRST_STEP_NUMBER = 1
ORDER_NUMBER_FORMAT = "ORD-{:03d}"
EXIT_CHOICE = "0"
YES_ANSWER = "д"
HANDLED_ERRORS = (CulinaryException, ValueError, TypeError, KeyError)


def create_system():
    """Создаёт пустую систему; всё состояние существует только в памяти."""
    warehouse = Warehouse(WAREHOUSE_NAME, WAREHOUSE_LOCATION, [], WAREHOUSE_CAPACITY_KG)
    return CulinarySystem(warehouse, Kitchen(KITCHEN_NAME))


class CulinaryConsole:
    """Консольное меню для управления складом и основными бизнес-процессами."""

    def __init__(self, system=None, read=None, write=None):
        self.system = system or create_system()
        self._read = read or input
        self._write = write or print

    def _ask(self, prompt):
        return self._read(prompt).strip()

    def _ask_number(self, prompt):
        return float(self._ask(prompt))

    def _ask_integer(self, prompt):
        return int(self._ask(prompt))

    def _main_actions(self):
        return {
            "1": ("Склад", self._warehouse_menu),
            "2": ("Рецепты", self._recipe_menu),
            "3": ("Меню блюд", self._menu_menu),
            "4": ("Заказы", self._order_menu),
            "5": ("Приготовление", self._cook_order),
            "6": ("Оплата и возврат", self._payment_menu),
            "7": ("Доставка", self._delivery_menu),
            "8": ("Отчёт по складу", self._stock_report),
        }

    def run(self):
        while self.run_once():
            pass
        self._write("Работа завершена.")

    def run_once(self):
        """Один шаг главного меню; возвращает False, если выбран выход."""
        actions = self._main_actions()
        self._write("\n=== Кулинарная система ===")
        for key, (title, _) in actions.items():
            self._write(f"{key}. {title}")
        self._write(f"{EXIT_CHOICE}. Выход")
        choice = self._ask("Выберите действие: ")
        if choice == EXIT_CHOICE:
            return False
        self._dispatch(actions, choice)
        return True

    def _dispatch(self, actions, choice):
        action = actions.get(choice)
        if action is None:
            self._write("Неизвестный пункт меню.")
            return
        try:
            action[1]()
        except HANDLED_ERRORS as error:
            self._write(f"Ошибка: {error}")

    def _submenu(self, title, actions):
        options = ", ".join(f"{key} — {label}" for key, (label, _) in actions.items())
        self._write(f"\n{title}: {options}")
        action = actions.get(self._ask("Действие: "))
        if action is None:
            self._write("Неизвестный пункт меню.")
            return
        action[1]()

    def _find_stock_item(self, name):
        stock_item = self.system.warehouse.get_stock_item(name)
        if stock_item is None:
            raise ValueError(f"Ингредиент «{name}» не найден")
        return stock_item

    def _warehouse_menu(self):
        self._submenu(
            "Склад",
            {
                "1": ("остатки", self._list_stock),
                "2": ("добавить продукт", self._add_stock),
                "3": ("пополнить", self._restock),
                "4": ("удалить пустую позицию", self._remove_stock),
            },
        )

    def _list_stock(self):
        items = self.system.warehouse.stock_items
        if not items:
            self._write("Склад пуст.")
        for item in items:
            self._write(f"{item.ingredient.name}: {item.quantity_kg:g} кг")

    def _read_ingredient_card(self, name, weight, allow_zero=False):
        return Ingredient(
            name,
            weight,
            self._ask_number("Цена за кг: "),
            self._ask_number("Калорийность на 100 г: "),
            self._ask_integer("Срок годности, дней: "),
            self._ask_number("Температура хранения: "),
            allow_zero=allow_zero,
        )

    def _add_stock(self):
        name = self._ask("Название: ")
        weight = self._ask_number("Количество, г: ")
        stock_item = self.system.add_ingredient(self._read_ingredient_card(name, weight))
        self._write(f"Добавлено: {stock_item.quantity_kg:g} кг")

    def _restock(self):
        stock_item = self._find_stock_item(self._ask("Название ингредиента: "))
        quantity_kg = self._ask_number("Поступление, кг: ")
        updated = self.system.restock_ingredient(stock_item.ingredient, quantity_kg)
        self._write(f"Остаток: {updated.quantity_kg:g} кг")

    def _remove_stock(self):
        name = self._ask("Название ингредиента: ")
        if not self.system.delete_ingredient(name):
            raise ValueError(f"Ингредиент «{name}» не найден")
        self._write("Пустая складская позиция удалена.")

    def _recipe_menu(self):
        self._submenu(
            "Рецепты",
            {
                "1": ("список", self._list_recipes),
                "2": ("создать", self._create_recipe),
                "3": ("изменить", self._update_recipe),
                "4": ("удалить", self._delete_recipe),
            },
        )

    def _list_recipes(self):
        for recipe in self.system.recipe_manager.recipes:
            self._write(f"{recipe.name}: {len(recipe.ingredients)} ингредиентов")

    def _resolve_ingredient(self, name):
        """Находит ингредиент на складе или в каталоге, иначе создаёт карточку без остатка."""
        ingredient = self.system.get_ingredient(name)
        if ingredient is not None:
            return ingredient
        self._write("Ингредиента нет в системе. Создаем карточку без остатка на складе.")
        ingredient = self._read_ingredient_card(name, 0, allow_zero=True)
        return self.system.register_ingredient(ingredient)

    def _read_recipe_ingredients(self, recipe):
        while True:
            name = self._ask("Ингредиент (пусто — завершить): ")
            if not name:
                break
            ingredient = self._resolve_ingredient(name)
            amount = self._ask_number("Количество: ")
            unit = self._ask("Единица (г/кг): ") or DEFAULT_UNIT
            recipe.add_ingredient(ingredient, amount, unit)
        if not recipe.ingredients:
            raise ValueError("В рецепте должен быть хотя бы один ингредиент")

    def _read_recipe(self, name=None):
        recipe = Recipe(
            name or self._ask("Название рецепта: "),
            self._ask("Описание: "),
            self._ask_integer("Время приготовления, мин: "),
            self._ask_integer("Количество порций: "),
        )
        self._read_recipe_ingredients(recipe)
        instruction = self._ask("Шаг приготовления: ")
        if instruction:
            recipe.add_step(RecipeStep(FIRST_STEP_NUMBER, instruction, recipe.preparation_minutes, None))
        return recipe

    def _create_recipe(self):
        self.system.add_recipe(self._read_recipe())
        self._write("Рецепт сохранен.")

    def _update_recipe(self):
        name = self._ask("Какой рецепт изменить: ")
        self.system.recipe_manager.find_recipe(name)
        self.system.update_recipe(name, self._read_recipe(name))
        self._write("Рецепт обновлен.")

    def _delete_recipe(self):
        name = self._ask("Какой рецепт удалить: ")
        if not self.system.delete_recipe(name):
            raise ValueError(f"Рецепт «{name}» не найден")
        self._write("Рецепт удален.")

    def _menu_menu(self):
        self._submenu(
            "Меню",
            {
                "1": ("список", self._list_menu),
                "2": ("добавить блюдо", self._add_dish),
                "3": ("доступность", self._set_availability),
            },
        )

    def _list_menu(self):
        for item in self.system.menu_items:
            availability = "доступно" if item.available else "недоступно"
            self._write(f"{item.dish.name}: {item.price:.2f} ({availability})")

    def _add_dish(self):
        recipe = self.system.recipe_manager.find_recipe(self._ask("Название рецепта: "))
        dish = Dish(recipe.name, recipe, recipe.servings, DEFAULT_DISH_TEMPERATURE)
        price = self._ask_number("Цена: ")
        category = self._ask("Категория: ") or DEFAULT_CATEGORY
        self.system.add_menu_item(MenuItem(dish, price, True, category))
        self._write("Блюдо добавлено в меню.")

    def _set_availability(self):
        name = self._ask("Название блюда: ")
        available = self._ask("Доступно? (д/н): ").casefold() == YES_ANSWER
        self.system.set_dish_availability(name, available)
        self._write("Доступность обновлена.")

    def _order_menu(self):
        self._submenu(
            "Заказы",
            {
                "1": ("список", self._list_orders),
                "2": ("создать", self._create_order),
                "3": ("изменить", self._edit_order),
                "4": ("отменить", self._cancel_order),
                "5": ("выдать (самовывоз)", self._hand_over_order),
            },
        )

    def _list_orders(self):
        for order in self.system.orders:
            self._write(f"{order.order_number}: {order.status}, {order.calculate_total():.2f}")

    def _read_order_items(self):
        items = []
        while True:
            name = self._ask("Блюдо (пусто — завершить): ")
            if not name:
                return items
            quantity = self._ask_integer("Количество порций: ")
            note = self._ask("Примечание: ")
            items.append(self.system.create_order_item(name, quantity, note))

    def _read_customer(self):
        return Customer(
            self._ask("Имя клиента: "),
            self._ask("Телефон: "),
            self._ask("Электронная почта: "),
            self._ask_integer("Возраст: "),
        )

    def _create_order(self):
        customer = self._read_customer()
        number = ORDER_NUMBER_FORMAT.format(len(self.system.orders) + 1)
        order = self.system.create_order(number, customer, self._read_order_items())
        self._write(f"Создан заказ {order.order_number}")

    def _edit_order(self):
        number = self._ask("Номер заказа: ")
        self.system.edit_order(number, self._read_order_items())
        self._write("Заказ обновлен.")

    def _cancel_order(self):
        self.system.cancel_order(self._ask("Номер заказа: "))
        self._write("Заказ отменен.")

    def _hand_over_order(self):
        order = self.system.hand_over_order(self._ask("Номер заказа: "))
        self._write(f"Заказ {order.order_number} выдан клиенту.")

    def _cook_order(self):
        order = self.system.cook_order(self._ask("Номер оплаченного заказа: "))
        self._write(f"Заказ приготовлен, статус: {order.status}")

    def _payment_menu(self):
        self._submenu(
            "Оплата",
            {
                "1": ("заказ", self._pay_order),
                "2": ("доставка", self._pay_delivery),
                "3": ("закупка", self._pay_purchase),
                "4": ("возврат оплаты заказа", self._refund_order),
            },
        )

    def _ask_payment_method(self):
        methods = "/".join(Payment.METHODS)
        return self._ask(f"Способ оплаты ({methods}): ") or DEFAULT_PAYMENT_METHOD

    def _pay_order(self):
        method = self._ask_payment_method()
        number = self._ask("Номер заказа: ")
        payment = self.system.pay_order(number, self._ask_number("Сумма: "), method)
        change = payment.amount - payment.charged_amount
        self._write(f"Оплачено, сдача: {change:.2f}")

    def _pay_delivery(self):
        method = self._ask_payment_method()
        number = self._ask("Номер заказа: ")
        self.system.pay_delivery(number, self._ask_number("Сумма доставки: "), method)
        self._write("Доставка оплачена отдельно.")

    def _read_purchase(self):
        ingredient = self._find_stock_item(self._ask("Название ингредиента: ")).ingredient
        quantity_kg = self._ask_number("Количество, кг: ")
        unit_price = self._ask_number("Цена за кг: ")
        supplier = Supplier(self._ask("Поставщик: "), self._ask("Телефон поставщика: "), [ingredient])
        return Purchase(supplier, ingredient, quantity_kg, unit_price)

    def _pay_purchase(self):
        method = self._ask_payment_method()
        purchase = self._read_purchase()
        self.system.pay_purchase(purchase, purchase.calculate_total(), method)
        self.system.receive_purchase(purchase)
        self._write("Закупка оплачена и принята на склад.")

    def _refund_order(self):
        refunded = self.system.refund_order(self._ask("Номер заказа: "))
        self._write(f"Возвращено клиенту: {refunded:.2f}")

    def _delivery_menu(self):
        self._submenu(
            "Доставка",
            {
                "1": ("оформить", self._create_delivery),
                "2": ("изменить статус", self._update_delivery),
            },
        )

    def _create_delivery(self):
        number = self._ask("Номер заказа: ")
        address = self._ask("Адрес: ")
        delivery = self.system.create_delivery(number, address, self._ask_number("Стоимость доставки: "))
        self._write(f"Доставка оформлена: {delivery.status}")

    def _update_delivery(self):
        number = self._ask("Номер заказа: ")
        statuses = "/".join(sorted(Delivery.STATUSES))
        delivery = self.system.update_delivery_status(number, self._ask(f"Новый статус ({statuses}): "))
        self._write(f"Статус доставки: {delivery.status}")

    def _stock_report(self):
        manager = InventoryManager(self.system.warehouse)
        for name, quantity_kg in manager.create_inventory_report().items():
            self._write(f"{name}: {quantity_kg:g} кг")
        self._write(f"Стоимость запасов: {manager.calculate_stock_value():.2f}")
        for name, shortage_kg in manager.calculate_reorder_quantities().items():
            self._write(f"Нужно дозаказать «{name}»: {shortage_kg:g} кг")
