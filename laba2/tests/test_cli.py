import pytest

import main
from cli.console import CulinaryConsole, create_system

INGREDIENT_CARD = ["200", "18", "7", "4"]
ADD_TOMATO = ["1", "2", "Помидор", "2000", *INGREDIENT_CARD]
ADD_RECIPE = ["2", "2", "Салат", "свежий", "10", "2", "Помидор", "200", "г", "", "Нарезать"]
ADD_DISH = ["3", "2", "Салат", "150", "салаты"]
CREATE_ORDER = ["4", "2", "Анна", "+7 900 000-00-00", "", "24", "Салат", "2", "без лука", ""]
PAY_ORDER = ["6", "1", "наличные", "ORD-001", "500"]
COOK = ["5", "ORD-001"]
PREPARED = ADD_TOMATO + ADD_RECIPE + ADD_DISH + CREATE_ORDER


def run_console(inputs, system=None):
    """Прогоняет сценарий меню; возвращает вывод и систему."""
    answers = iter([*inputs, "0"])
    output = []
    console = CulinaryConsole(system, read=lambda prompt: next(answers), write=output.append)
    console.run()
    return "\n".join(output), console.system


class TestCulinaryConsole:
    def test_exit_and_unknown_choice(self):
        output, _ = run_console(["9", "1", "7"])
        assert output.count("Неизвестный пункт меню.") == 2 and output.endswith("Работа завершена.")

    def test_create_system(self):
        system = create_system()
        assert system.warehouse.capacity_kg == 10000 and system.kitchen.is_clean()

    def test_warehouse_menu(self):
        output, system = run_console(["1", "1", *ADD_TOMATO, "1", "1", "1", "3", "Помидор", "1", "1", "4", "Лук"])
        assert "Склад пуст." in output and "Добавлено: 2 кг" in output
        assert "Помидор: 2 кг" in output and "Остаток: 3 кг" in output
        assert "Ошибка: Ингредиент «Лук» не найден" in output
        assert system.warehouse.get_available_quantity("Помидор") == 3

    def test_remove_empty_stock_and_unknown_restock(self):
        system = create_system()
        output, _ = run_console(["1", "3", "Лук"], system)
        assert "Ошибка: Ингредиент «Лук» не найден" in output
        from culinary.ingredients import Ingredient

        system.add_ingredient(Ingredient("Соль", 0, 40, 0, 30, 20, allow_zero=True))
        output, _ = run_console(["1", "4", "Соль"], system)
        assert "Пустая складская позиция удалена." in output

    def test_recipe_menu(self):
        new_ingredient = ["Укроп", *INGREDIENT_CARD, "10", ""]
        update = ["2", "3", "Салат", "новый", "5", "2", "Помидор", "0.1", "кг", *new_ingredient, "", ""]
        script = ADD_TOMATO + ADD_RECIPE + update + ["2", "1", "2", "4", "Салат", "2", "4", "Суп"]
        output, system = run_console(script)
        assert "Рецепт сохранен." in output and "Рецепт обновлен." in output
        assert "Ингредиента нет в системе" in output and "Салат: 2 ингредиентов" in output
        assert "Рецепт удален." in output and "Ошибка: Рецепт «Суп» не найден" in output
        assert system.get_ingredient("Укроп").weight == 0

    def test_recipe_requires_ingredients(self):
        output, _ = run_console(["2", "2", "Суп", "", "10", "1", ""])
        assert "Ошибка: В рецепте должен быть хотя бы один ингредиент" in output

    def test_menu_menu(self):
        script = (
            ADD_TOMATO + ADD_RECIPE + ADD_DISH + ["3", "3", "Салат", "н", "3", "1", "3", "3", "Салат", "д", "3", "1"]
        )
        output, system = run_console(script)
        assert "Блюдо добавлено в меню." in output and "Доступность обновлена." in output
        assert "Салат: 150.00 (недоступно)" in output and "Салат: 150.00 (доступно)" in output
        assert system.menu_items[0].category == "салаты"

    def test_order_menu(self):
        edit = ["4", "3", "ORD-001", "Салат", "1", "", ""]
        script = PREPARED + ["4", "1"] + edit + ["4", "4", "ORD-001", "4", "5", "ORD-001"]
        output, system = run_console(script)
        assert "Создан заказ ORD-001" in output and "ORD-001: новый, 300.00" in output
        assert "Заказ обновлен." in output and "Заказ отменен." in output
        assert "Ошибка: Выдать можно только готовый заказ" in output
        assert system.get_order("ORD-001").status == "отменён"

    def test_payment_cooking_and_pickup(self):
        script = PREPARED + PAY_ORDER + COOK + ["4", "5", "ORD-001"]
        output, system = run_console(script)
        assert "Оплачено, сдача: 200.00" in output and "Заказ приготовлен, статус: готов" in output
        assert "Заказ ORD-001 выдан клиенту." in output

    def test_refund(self):
        output, _ = run_console(PREPARED + PAY_ORDER + ["6", "4", "ORD-001"])
        assert "Возвращено клиенту: 300.00" in output

    def test_delivery(self):
        create = ["7", "1", "ORD-001", "ул. Мира, 5", "100"]
        pay = ["6", "2", "онлайн", "ORD-001", "100"]
        statuses = [step for status in ("готовится", "в пути", "доставлен") for step in ("7", "2", "ORD-001", status)]
        output, system = run_console(PREPARED + PAY_ORDER + COOK + create + pay + statuses)
        assert "Доставка оформлена: ожидает" in output and "Доставка оплачена отдельно." in output
        assert "Статус доставки: доставлен" in output and system.get_order("ORD-001").status == "выдан"

    def test_purchase_and_report(self):
        purchase = ["6", "3", "", "Помидор", "2", "180", "Ферма", "+7 900 777-77-77"]
        output, system = run_console(ADD_TOMATO + purchase + ["8"])
        assert "Закупка оплачена и принята на склад." in output
        assert "Помидор: 4 кг" in output and "Стоимость запасов: 800.00" in output
        assert system.warehouse.get_available_quantity("Помидор") == 4

    def test_report_shows_reorder(self):
        system = create_system()
        from culinary.ingredients import Ingredient

        system.add_ingredient(Ingredient("Соль", 500, 40, 0, 30, 20), minimum_kg=2)
        output, _ = run_console(["8"], system)
        assert "Нужно дозаказать «Соль»: 1.5 кг" in output

    def test_invalid_number_is_reported(self):
        output, _ = run_console(["1", "2", "Помидор", "много"])
        assert "Ошибка: could not convert string to float" in output


class TestMain:
    def test_main_handles_end_of_input(self, monkeypatch, capsys):
        def end_of_input(prompt):
            raise EOFError

        monkeypatch.setattr("builtins.input", end_of_input)
        main.main()
        assert "Работа завершена." in capsys.readouterr().out

    def test_main_runs_console(self, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", lambda prompt: "0")
        main.main()
        assert "=== Кулинарная система ===" in capsys.readouterr().out


@pytest.mark.parametrize("choice", ["1", "2", "3", "4", "6", "7"])
def test_every_submenu_rejects_unknown_action(choice):
    output, _ = run_console([choice, "99"])
    assert "Неизвестный пункт меню." in output
