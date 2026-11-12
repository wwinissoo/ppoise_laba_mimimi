"""Консольная точка входа для демонстрации объектной модели кулинарии."""
from datetime import datetime
from culinary.people.customer import Customer
from culinary.recipes.recipe import Recipe
from culinary.ingredients.vegetable import Vegetable
from culinary.recipes.recipe_step import RecipeStep
from culinary.dishes.dish import Dish
from culinary.orders.order_item import OrderItem
from culinary.orders.order import Order
from culinary.orders.payment import Payment
from culinary.orders.receipt import Receipt
from culinary.exceptions import CulinaryError


def create_demo_order():
    """Создаёт и демонстрирует связанный набор объектов предметной области."""
    customer = Customer("Анна", "+7 900 000-00-00", "anna@example.com", 24, 30)
    tomato = Vegetable("Помидор", 1000, 180, 18, 7, 4, is_organic=True)
    recipe = Recipe("Овощной салат", "Простой салат из свежих овощей", 10, 2)
    recipe.add_ingredient(tomato, 200, "г")
    recipe.add_step(RecipeStep(1, "Помыть и нарезать помидоры", 5, None))
    recipe.add_step(RecipeStep(2, "Заправить и перемешать салат", 5, None))
    dish = Dish("Овощной салат", recipe, 2, 12)
    item = OrderItem(dish, 2, 150.0, "Без лука")
    order = Order("ORD-001", customer, [item], "новый", datetime.now())
    payment = Payment(order, order.calculate_total(), "карта", "ожидает")
    change = payment.process()
    receipt = Receipt(order, payment, "RC-001", False)
    receipt.issue()
    return order, payment, receipt, change


def show_menu():
    """Запускает текстовое меню приложения."""
    while True:
        print("\n=== Кулинарная система ===")
        print("1. Создать демонстрационный заказ")
        print("2. Показать доступные разделы модели")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                order, payment, receipt, change = create_demo_order()
                print(f"Заказ: {order.order_number}")
                print(f"Клиент: {order.customer.name}")
                print(f"Сумма: {order.calculate_total():.2f}")
                print(f"Статус оплаты: {payment.status}")
                print(f"Чек: {receipt.receipt_number}, выдан: {receipt.issued}")
                print(f"Сдача: {change:.2f}")
            elif choice == "2":
                print("Разделы: ingredients, recipes, dishes, kitchen, warehouse, people, orders, nutrition, exceptions")
            elif choice == "0":
                print("Работа завершена.")
                break
            else:
                print("Неизвестный пункт меню.")
        except (CulinaryError, ValueError, TypeError, AttributeError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    show_menu()
