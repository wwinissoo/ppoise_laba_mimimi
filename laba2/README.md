# Лабораторная работа №2: «Кулинария» (Culinary System)

## 1. Назначение проекта

Проект представляет собой объектно-ориентированную систему автоматизации кулинарного производства, складского учета, работы кухни и обслуживания клиентов в ресторане. 

Система охватывает весь жизненный цикл процессов:
- Учет ингредиентов и складских партий с контролем сроков годности.
- Формирование рецептур, технологических карт и шагов приготовления.
- Моделирование работы кухонного оборудования, инвентаря и поваров.
- Расчет калорийности, пищевой ценности и отслеживание аллергенов.
- Прием заказов клиентов, их оплату, чеки и доставку.
- Обработку нештатных ситуаций через предметную иерархию исключений.

---

## 2. Структура проекта

```text
laba2/
├── culinary/
│   ├── __init__.py
│   ├── dishes/              # Блюда, меню, порции и категории блюд
│   ├── exceptions/          # Иерархия пользовательских исключений
│   ├── ingredients/         # Базовый класс ингредиентов и их разновидности
│   ├── kitchen/             # Оборудование кухни, инструменты и рабочие зоны
│   ├── nutrition/           # Пищевая ценность, калории, нутриенты, аллергены
│   ├── orders/              # Заказы клиентов, чеки, оплата и логистика
│   ├── people/              # Персонал ресторана, повара, клиенты
│   ├── recipes/             # Рецепты, шаги приготовления, кулинарные книги
│   └── warehouse/           # Складской учет, партии товаров, поставщики
├── tests/                   # Набор юнит-тестов (pytest)
├── main.py                  # Точка входа в приложение
├── pytest.ini               # Конфигурационный файл pytest
├── requirements.txt         # Зависимости проекта
└── README.md                # Документация проекта
```

---

## 3. Подробное описание модулей и классов

### 3.1. Ингредиенты (`culinary.ingredients`)

* **`Ingredient`** *(Абстрактный базовый класс)*:
  * **Назначение**: Базовый класс для всех типов продуктов и ингредиентов.
  * **Поля**: `name` (str), `unit` (str), `calories_per_unit` (float), `is_allergen` (bool).
  * **Методы**: `get_info()`, `calculate_calories(amount: float)`.
* **`DairyProduct`** *(наследуется от `Ingredient`)*: Молочные продукты (жирность, лактоза).
* **`Egg`** *(наследуется от `Ingredient`)*: Яйца (категория, тип).
* **`Fish`** *(наследуется от `Ingredient`)*: Рыба и морепродукты (вид, тип разделки).
* **`Flour`** *(наследуется от `Ingredient`)*: Мука и зерновые продукты (сорт, клейковина).
* **`Fruit`** *(наследуется от `Ingredient`)*: Фрукты и ягоды (содержание сахара, свежесть).
* **`Meat`** *(наследуется от `Ingredient`)*: Мясо и птица (вид мяса, часть туши).
* **`Oil`** *(наследуется от `Ingredient`)*: Масла и жиры (тип отжима, температура горения).
* **`Spice`** *(наследуется от `Ingredient`)*: Специи и пряности (острота, степень помола).
* **`Vegetable`** *(наследуется от `Ingredient`)*: Овощи (способ обработки, тип).

### 3.2. Рецепты (`culinary.recipes`)

* **`Recipe`**:
  * **Назначение**: Технологическая карта блюда.
  * **Поля**: `name` (str), `category` (RecipeCategory), `ingredients` (list[RecipeIngredient]), `steps` (list[RecipeStep]), `cooking_time` (CookingTime).
  * **Методы**: `add_ingredient()`, `add_step()`, `get_total_time()`, `calculate_total_calories()`.
* **`RecipeIngredient`**: Связывает `Ingredient` с необходимым для рецепта количеством (`amount`) и единицами измерения.
* **`RecipeStep` / `CookingInstruction`**: Описывают отдельный шаг приготовления (действие, время, требуемое оборудование).
* **`CookingTime`**: Учитывает время подготовки (`prep_time`) и время термообработки (`cook_time`).
* **`RecipeBook`**: Хранилище рецептов с возможностью поиска по названию, категории или ингредиентам.
* **`RecipeManager`**: Сервисный класс для добавления, валидации и управления рецептами.
* **`RecipeCategory`**: Перечисление/класс категорий рецептов (первые блюда, десерты и т.д.).
* **`Serving`**: Описывает количество порций и правила подачи.

### 3.3. Блюда (`culinary.dishes`)

* **`Dish`** *(Базовый класс)*:
  * **Назначение**: Готовое кулинарное изделие на основе рецепта.
  * **Поля**: `name` (str), `recipe` (Recipe), `price` (float), `weight` (float), `nutrition_facts` (NutritionFacts).
  * **Методы**: `calculate_price()`, `get_allergens()`, `display_card()`.
* **Наследники `Dish`**:
  * `Beverage` (напитки)
  * `Dessert` (десерты)
  * `Garnish` (гарниры)
  * `MainCourse` (основные горячие блюда)
  * `Pastry` (выпечка)
  * `Salad` (салаты)
  * `Sauce` (соусы)
  * `Soup` (супы)
* **`Portion`**: Управление размером порции (детская, стандартная, большая) и коэффициентами перерасчета.
* **`Menu`** и **`MenuItem`**: Ресторанное меню, содержащее список доступных блюд, цены и статусы доступности.

### 3.4. Кухня (`culinary.kitchen`)

* **`Kitchen`**:
  * **Назначение**: Главный координационный центр приготовления пищи.
  * **Поля**: `workstations` (list[Workstation]), `inventory` (KitchenInventory), `staff` (list[Person]).
  * **Методы**: `assign_cook()`, `cook_dish(recipe, cook)`, `check_equipment_availability()`.
* **`Workstation`**: Рабочее место (холодный цех, горячий цех, кондитерский цех).
* **`CookingEquipment`** / **`KitchenTool`**: Базовые классы для кухонной техники и инвентаря.
* **Специализированная техника**:
  * `Blender` — измельчение и смешивание.
  * `FryingPan` — обжарка.
  * `Oven` — запекание, выпечка.
  * `Refrigerator` — охлаждение и хранение.
  * `Saucepan` — варка и тушение.
  * `Stove` — плита (варочная панель).
* **`KitchenInventory`**: Реестр наличных кухонных приборов и оборудования.

### 3.5. Склад (`culinary.warehouse`)

* **`Warehouse`**:
  * **Назначение**: Управление запасами сырья и материалов.
  * **Поля**: `capacity` (float), `stocks` (dict), `suppliers` (list[Supplier]).
  * **Методы**: `accept_delivery(batch)`, `deduct_ingredient(ingredient, amount)`, `get_available_quantity()`.
* **`ProductBatch`**: Партия товара (дата поставки, срок годности, объем).
* **`Stock` / `StockItem`**: Текущие остатки конкретных ингредиентов.
* **`Supplier`**: Информация о поставщике.
* **`Purchase`**: Заказ на закупку товаров у поставщика.
* **`Delivery`**: Акты приемки и доставки сырья.
* **`ExpirationTracker`**: Автоматический отслеживатель просроченных товаров на складе.

### 3.6. Персонал (`culinary.people`)

* **`Person`** *(Базовый класс)*:
  * **Поля**: `id` (int), `name` (str), `phone` (str).
* **`Chef`**: Шеф-повар, управляет меню и разработкой рецептов.
* **`ChefSpecialization`**: Специализация повара (соусье, кондитер, су-шеф).
* **`Cook`**: Повар, исполняющий технологические шаги рецепта.
* **`KitchenAssistant` / `KitchenWorker`**: Вспомогательный персонал кухни.
* **`Customer`**: Посетитель/клиент ресторана (диетологические предпочтения, баланс).
* **`Nutritionist`**: Диетолог, составляющий планы питания.

### 3.7. Заказы (`culinary.orders`)

* **`Order` / `CustomerOrder`**:
  * **Назначение**: Оформление и отслеживание статуса заказа клиента.
  * **Поля**: `order_id` (str), `customer` (Customer), `items` (list[OrderItem]), `status` (OrderStatus), `total_amount` (float).
  * **Методы**: `add_item()`, `remove_item()`, `calculate_total()`, `change_status()`.
* **`OrderItem`**: Элемент заказа с указанием блюда и количества.
* **`Payment`**: Проведение оплаты (наличные, карта, онлайн).
* **`Receipt`**: Генерация кассового чека.
* **`Delivery`**: Организация курьерской доставки заказа.

### 3.8. Пищевая ценность (`culinary.nutrition`)

* **`Nutrient`**: Отдельный нутриент (белки, жиры, углеводы, витамины).
* **`NutritionFacts` / `NutritionValue`**: Полный расчет БЖУ и калорийности на 100г и на порцию.
* **`Allergen`**: Реестр потенциальных аллергенов (глютен, орехи, лактоза и т.д.).
* **`CalorieCalculator`**: Калькулятор общей калорийности по списку ингредиентов.
* **`DietPlan` / `DietaryPlan`**: Диетические программы (веганская, низкоуглеводная и т.д.).

---

## 4. Иерархия исключений (`culinary.exceptions`)

Система содержит разветвленную иерархию пользовательских исключений, унаследованных от базового `CulinaryException` (или `CulinaryError`):

```text
CulinaryException (CulinaryError)
├── InvalidIngredientException / InvalidIngredientError
├── ExpiredIngredientException / ExpiredIngredientError
├── InsufficientIngredientException / InsufficientIngredientError
├── InvalidRecipeException
├── RecipeNotFoundError
├── InvalidRecipeStepError
├── DishUnavailableError
├── KitchenEquipmentError
├── UnavailableToolException
├── WarehouseCapacityError
├── InsufficientStockException
├── ExpiredProductException
├── InvalidOrderException
├── OrderStateError
├── PaymentException / PaymentError
├── PortionException
├── InvalidTemperatureException
├── AllergenException
└── SupplierError
```

Примеры обработки:
- `WarehouseCapacityError`: Вызывается при попытке принять партию товара, превышающую лимит склада.
- `ExpiredIngredientException`: Блокирует приготовление блюда, если используемый ингредиент просрочен.
- `InsufficientIngredientException`: Возникает при отсутствии нужного количества ингредиентов на складе.

---

## 5. Связи и ассоциации между классами

1. **Композиция**:
   * `Recipe` содержит `RecipeStep` и `RecipeIngredient`.
   * `Order` содержит `OrderItem`.
   * `Warehouse` содержит `Stock`.
2. **Агрегация**:
   * `Dish` ссылается на `Recipe`.
   * `Kitchen` содержит список `Workstation` и `CookingEquipment`.
   * `Menu` содержит список `MenuItem`.
3. **Наследование**:
   * Все типы ингредиентов (`DairyProduct`, `Meat` и др.) наследуют абстрактный класс `Ingredient`.
   * Разновидности блюд (`Soup`, `Dessert` и др.) наследуют `Dish`.
   * Весь персонал наследует `Person`.

---

## 6. Запуск программы и тестов

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск основного приложения
```bash
python main.py
```

### Запуск модульных тестов
```bash
pytest
```

---

## 7. Соответствие требованиям лабораторной работы

* **Принципы ООП**: Реализованы наследование, инкапсуляция и полиморфизм.
* **Модульность**: Проект разбита на 9 предметных пакетов.
* **Исключения**: Использовано 12+ специализированных классов ошибок.
* **Тестирование**: Модуль `tests/` покрывает функциональность всех ключевых элементов системы.