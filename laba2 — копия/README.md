# Лабораторная работа №2: «Кулинария» (Culinary System)

## 1. Назначение проекта

Объектная модель ресторанной кухни: учёт ингредиентов и склада, рецепты и
технологические карты, блюда и меню, кухонное оборудование, персонал,
пищевая ценность и аллергены, заказы клиентов, оплата, чеки и доставка.
Предметная область (`culinary/`) полностью отделена от консольного интерфейса
(`cli/`); всё состояние хранится в памяти текущего запуска.

## 2. Сборка, запуск и тесты (только консоль, без IDE)

```bash
cd laba2
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt   # pytest, pytest-cov, flake8, black

.venv/bin/python main.py                         # консольное меню
.venv/bin/python -m pytest                       # тесты + покрытие (порог 90 %)
.venv/bin/flake8 .                               # статический анализ
.venv/bin/black --check culinary cli main.py build.py tests   # единый стиль
.venv/bin/python build.py                        # артефакт dist/culinary-lab2.pyz
python3 dist/culinary-lab2.pyz                   # запуск собранного артефакта
```

Артефакт `culinary-lab2.pyz` — самодостаточный zip-архив Python (модуль `zipapp`):
для запуска нужен только Python 3.11+, без установки зависимостей и без исходников.

## 3. Структура проекта

```text
laba2/
├── culinary/                # предметная область (не знает о консоли)
│   ├── application.py       # CulinarySystem — фасад бизнес-процессов
│   ├── validation.py        # общие проверки входных данных и переходов статусов
│   ├── units.py             # единицы измерения и коэффициенты пересчёта
│   ├── ingredients/         # Ingredient и 9 разновидностей продуктов
│   ├── recipes/             # Recipe, RecipeIngredient, шаги, книги, категории
│   ├── dishes/              # Dish и наследники, гарнир, соус, порция, меню
│   ├── kitchen/             # Kitchen, оборудование, инструменты, рабочие места
│   ├── nutrition/           # аллергены, нутриенты, КБЖУ, план питания
│   ├── people/              # Person и наследники, специализация шефа
│   ├── orders/              # Order, OrderItem, Payment, Receipt, Delivery
│   ├── warehouse/           # Warehouse, StockItem, поставщики, закупки, партии
│   └── exceptions/          # иерархия собственных исключений
├── cli/console.py           # CulinaryConsole — меню, только ввод/вывод
├── main.py                  # точка входа
├── build.py                 # сборка исполняемого артефакта
├── tests/                   # pytest: отдельный Test-класс на каждый класс модели
├── pytest.ini               # запуск тестов с покрытием и порогом 90 %
├── pyproject.toml, .flake8  # настройки black, coverage, flake8
├── requirements.txt         # зависимости для тестов
└── requirements-dev.txt     # + линтеры
```

CI/CD-пайплайн: `.github/workflows/laba2.yaml` в корне репозитория (раздел 10).

## 4. Соответствие количественным требованиям

| Требование | Минимум | Фактически |
|---|---|---|
| Классы | 50 | **96** (72 класса предметной области + 24 исключения) |
| Поля (суммарно, без исключений) | 150 | **245** |
| Уникальные поведения (методы, не геттеры/сеттеры) | 100 | **293** уникальных по имени, 317 всего |
| Ассоциации между классами | 30 | **50** (см. раздел 6) |
| Собственные исключения | 12 | **24** (см. раздел 7) |

Псевдонимы `NutritionValue = Nutrient`, `DietaryPlan = DietPlan`,
`culinary.orders.Menu/MenuItem` и `culinary.warehouse.Delivery = SupplierDelivery`
оставлены только для совместимости импортов и **не считаются** отдельными классами.

Все поля хранятся в приватных атрибутах (`self.__field`) и доступны через
свойства только для чтения; коллекции наружу отдаются кортежами (`tuple`),
поэтому изменить их можно только методами класса с проверками.

## 5. Классы, поля и методы

В таблицах перечислены поля (инициализируются в `__init__`, доступны через
свойства) и методы с поведением предметной области. Свойства-геттеры не перечисляются.

### 5.1. Ингредиенты (`culinary.ingredients`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `DairyProduct` | Ingredient | fat_percentage, lactose_free, fermentation_required, is_fermented | `ferment`, `calculate_fat_weight`, `is_suitable_for_lactose_free_diet`, `check_fermentation` |
| `Egg` | Ingredient | egg_size, shell_intact, yolk_color, is_cracked | `crack`, `check_shell`, `change_yolk_color_label`, `is_suitable_for_boiling` |
| `Fish` | Ingredient | fish_type, has_scales, bone_count, is_cleaned | `remove_scales`, `remove_bones`, `clean_fish`, `is_ready_for_cooking` |
| `Flour` | Ingredient | protein_percentage, gluten_content, flour_type, is_sifted | `sift`, `calculate_protein_weight`, `is_suitable_for_bread`, `change_flour_type` |
| `Fruit` | Ingredient | sweetness, has_seeds, is_ripe, is_cut | `ripen`, `cut`, `calculate_sweetness_score`, `remove_seeds` |
| `Ingredient` | — | name, initial_weight, weight, price_per_kg, calories, expiration_days, storage_temperature, is_available, days_passed | `calculate_cost`, `calculate_calories`, `consume`, `receive`, `check_expiration`, `require_fresh`, `pass_day`, `calculate_remaining_percentage`, `update_price`, `update_storage_temperature` |
| `Meat` | Ingredient | fat_percentage, meat_type, is_frozen, is_marinated | `defrost`, `marinate`, `calculate_fat_weight`, `check_fat_content` |
| `Oil` | Ingredient | smoke_point, is_refined, oil_type, is_heated | `heat`, `is_suitable_for_frying`, `calculate_remaining_after_frying`, `classify_refinement` |
| `Spice` | Ingredient | intensity, flavor, is_ground, is_mixed | `grind`, `mix_with`, `adjust_intensity`, `describe_flavor` |
| `Vegetable` | Ingredient | is_organic, requires_peeling, water_percentage, is_washed, is_peeled | `wash`, `peel`, `calculate_clean_weight`, `is_suitable_for_salad` |

### 5.2. Рецепты (`culinary.recipes`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `CookingInstruction` | — | title, text, difficulty, safety_note | `validate_text`, `shorten`, `has_safety_warning` |
| `CookingTime` | — | preparation, cooking, resting, unit | `total_minutes`, `is_quick_recipe`, `add_resting_time` |
| `Recipe` | — | name, description, preparation_minutes, servings, ingredients, steps | `add_ingredient`, `remove_ingredient`, `has_ingredient`, `add_step`, `calculate_requirements`, `calculate_steps_duration`, `estimate_total_cost`, `calculate_total_calories`, `scale_servings`, `format_steps` |
| `RecipeBook` | — | title, author, recipes | `add_recipe`, `find_by_name`, `get_by_name`, `find_by_ingredient`, `count_recipes` |
| `RecipeCategory` | — | name, description, recipes, dietary_tag | `add_recipe`, `remove_recipe`, `matches_diet` |
| `RecipeIngredient` | — | ingredient, amount, unit, is_optional | `to_grams`, `to_kilograms`, `amount_in_grams`, `amount_in_kilograms`, `calculate_cost`, `calculate_calories`, `consume_from_stock`, `describe_amount` |
| `RecipeManager` | — | recipes | `add_recipe`, `update_recipe`, `find_recipe`, `remove_recipe`, `search_by_ingredient` |
| `RecipeStep` | — | number, instruction, duration_minutes, temperature | `format_instruction`, `calculate_end_minute` |
| `Serving` | — | temperature_celsius, presentation, serving_size_grams | `describe`, `calculate_total_weight` |

### 5.3. Блюда (`culinary.dishes`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `Beverage` | Dish | volume_ml, is_carbonated | `dilute`, `serving_volume` |
| `Dessert` | Dish | sugar_grams, chilled | `calculate_sugar_per_portion`, `is_low_sugar`, `chill` |
| `Dish` | — | name, recipe, portions, serving_temperature | `prepare`, `calculate_cost_per_portion`, `calculate_calories_per_portion`, `change_serving_temperature`, `replace_recipe` |
| `Garnish` | — | name, weight, decoration_style, ingredients | `add_ingredient`, `calculate_ingredient_weight`, `is_light_garnish` |
| `MainCourse` | Dish | side_dish | `attach_side_dish`, `has_side_dish` |
| `Menu` | — | title, valid_from, valid_to, dishes | `add_dish`, `remove_dish`, `find_dish`, `find_dishes_under_price`, `is_active` |
| `MenuItem` | — | dish, price, available, category | `mark_unavailable`, `mark_available`, `apply_discount`, `calculate_margin`, `require_available` |
| `Pastry` | Dish | baking_temperature, baking_minutes | `estimate_baking_end`, `can_bake_in` |
| `Portion` | — | dish, weight, price, table_number | `calculate_price_per_gram`, `is_for_table`, `increase_weight` |
| `Salad` | Dish | dressing | `add_dressing`, `is_served_chilled` |
| `Sauce` | — | name, base_ingredient, consistency, volume | `thicken`, `dilute`, `reduce`, `is_based_on` |
| `Soup` | Dish | broth, extra_components | `add_component`, `count_components`, `is_hot_enough` |

### 5.4. Кухня (`culinary.kitchen`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `Blender` | CookingEquipment | max_speed | `validate_speed`, `blend_time` |
| `CookingEquipment` | — | name, power_watts, status, last_service_days | `is_operational`, `turn_on`, `turn_off`, `mark_broken`, `pass_days`, `needs_service`, `record_service` |
| `FryingPan` | KitchenTool | diameter_cm | `suitable_for_portions`, `recommend_heat` |
| `Kitchen` | — | name, cleanliness_level, workstations, equipment | `add_workstation`, `register_equipment`, `find_free_workstation`, `is_clean`, `soil`, `record_cleaning`, `check_readiness`, `validate_recipe`, `cook_recipe` |
| `KitchenInventory` | — | tools, equipment | `register_tool`, `register_equipment`, `count_items`, `find_unavailable`, `find_needing_service` |
| `KitchenTool` | — | name, material, condition, is_clean | `clean`, `use`, `mark_damaged`, `repair`, `is_usable` |
| `Oven` | CookingEquipment | max_temperature, current_temperature | `preheat`, `bake`, `turn_off`, `estimate_energy_kwh` |
| `Refrigerator` | CookingEquipment | temperature | `set_temperature`, `is_freezing`, `can_store`, `estimate_daily_energy` |
| `Saucepan` | KitchenTool | capacity_liters | `can_hold`, `fill_percentage` |
| `Stove` | CookingEquipment | burner_count | `can_use_burners`, `estimate_energy` |
| `Workstation` | — | number, assigned_worker, is_occupied, tools | `assign_worker`, `release`, `add_tool`, `find_unusable_tools` |

### 5.5. Питание (`culinary.nutrition`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `Allergen` | — | name, severity, description | `matches_ingredient`, `find_in_recipe`, `ensure_absent`, `describe` |
| `CalorieCalculator` | — | — | `calculate_ingredient`, `calculate_recipe`, `calculate_per_serving`, `calculate_daily_balance` |
| `DietPlan` | — | title, excluded_ingredients, daily_calorie_limit, meals | `is_ingredient_allowed`, `is_dish_allowed`, `add_meal`, `calculate_daily_calories`, `is_within_limit`, `remaining_calories` |
| `Nutrient` | — | name, amount_grams, daily_value_grams, unit | `daily_value_percentage`, `is_deficient`, `convert_to_milligrams`, `amount_in_display_unit` |
| `NutritionFacts` | — | calories, protein, fat, carbohydrates, serving_grams | `calculate_energy_from_macros`, `scale_to_serving`, `is_high_protein` |

### 5.6. Люди (`culinary.people`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `Chef` | Person | specialization, experience_years | `is_qualified`, `can_prepare`, `prepare_recipe`, `add_experience` |
| `ChefSpecialization` | — | title, allowed_categories, certification_level, years_required | `allows`, `is_certified`, `experience_requirement_met` |
| `Cook` | Person | shift_hours, skill_level | `estimate_shift_end`, `improve_skill` |
| `Customer` | Person | loyalty_points, allergies | `add_loyalty_points`, `spend_loyalty_points`, `earn_points_for_purchase`, `add_allergy`, `ensure_can_eat` |
| `KitchenAssistant` | Person | assigned_area | `change_area`, `prepare_work_area`, `count_unclean_tools` |
| `KitchenWorker` | Person | position, shift_hours | `change_position`, `extend_shift`, `finish_shift` |
| `Nutritionist` | Person | qualification, experience_years | `review_plan`, `add_experience` |
| `Person` | — | name, phone, email, age | `change_phone`, `has_valid_contact`, `is_adult` |

### 5.7. Заказы (`culinary.orders`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `CustomerOrder` | — | customer, order, delivery_address, delivery_required | `request_delivery`, `cancel_delivery`, `get_customer_name` |
| `Delivery` | — | order, address, delivery_fee, status | `calculate_total`, `update_status`, `is_completed`, `is_cancelled` |
| `Order` | — | order_number, customer, items, status, created_at | `add_item`, `remove_item`, `replace_items`, `calculate_total`, `count_portions`, `change_status` |
| `OrderItem` | — | dish, quantity, unit_price, note | `calculate_total`, `increase_quantity`, `update_quantity`, `update_unit_price`, `add_note` |
| `Payment` | — | order, amount, method, status, purpose, expected_amount, charged_amount | `process`, `refund`, `is_paid`, `is_refunded` |
| `Receipt` | — | order, payment, receipt_number, issued | `issue`, `format_total`, `format_lines`, `void` |

### 5.8. Склад (`culinary.warehouse`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `ExpirationTracker` | — | ingredients | `register`, `advance_day`, `expired_items`, `fresh_items`, `expiring_within` |
| `Inventory` | — | warehouse, counted_by, inventory_date, counted_items | `record_count`, `find_discrepancies`, `find_uncounted`, `is_balanced` |
| `InventoryManager` | — | warehouse | `calculate_stock_value`, `find_reorder_candidates`, `calculate_reorder_quantities`, `create_inventory_report` |
| `ProductBatch` | — | ingredient, batch_code, received_date, quantity_kg, supplier, used_kg | `is_expired`, `use`, `remaining_quantity`, `assign_batch_code` |
| `Purchase` | — | supplier, ingredient, quantity_kg, unit_price, status | `calculate_total`, `mark_paid`, `mark_received`, `cancel` |
| `Stock` | — | items | `add_item`, `get_item`, `total_quantity`, `below_minimum` |
| `StockItem` | — | ingredient, quantity_kg, minimum_kg, location_code | `needs_restock`, `calculate_shortage`, `withdraw`, `receive`, `relocate` |
| `Supplier` | — | name, phone, rating, products | `add_product`, `rate`, `is_reliable`, `supplies` |
| `SupplierDelivery` | — | supplier, delivery_date, status, batches | `add_batch`, `dispatch`, `mark_received`, `cancel`, `calculate_delivered_weight` |
| `Warehouse` | — | name, location, capacity_kg, stock_items | `calculate_total_weight`, `calculate_free_capacity`, `has_free_capacity`, `add_stock_item`, `remove_stock_item`, `get_stock_item`, `get_available_quantity`, `find_expired`, `write_off_expired`, `deduct_ingredient` |

### 5.9. Фасад (`culinary.application`)

| Класс | Родитель | Поля | Методы (поведение) |
|---|---|---|---|
| `CulinarySystem` | — | warehouse, kitchen, recipe_manager, menu_items, orders, order_payments, delivery_payments, deliveries, purchase_payments, ingredients | `register_ingredient`, `add_ingredient`, `get_ingredient`, `restock_ingredient`, `delete_ingredient`, `add_recipe`, `update_recipe`, `delete_recipe`, `add_menu_item`, `set_dish_availability`, `create_order_item`, `create_order`, `get_order`, `edit_order`, `pay_order`, `refund_order`, `cancel_order`, `pay_purchase`, `receive_purchase`, `pay_delivery`, `cook_order`, `hand_over_order`, `create_delivery`, `update_delivery_status` |

## 6. Ассоциации между классами

Ассоциация — класс хранит другой класс в поле или принимает его параметром метода.
Типы ассоциаций проверяются через `isinstance`.

| № | Класс | Связан с | Вид |
|---|---|---|---|
| 1 | `RecipeIngredient` | `Ingredient` | поле `ingredient` |
| 2 | `Recipe` | `RecipeIngredient` | композиция, `ingredients` |
| 3 | `Recipe` | `RecipeStep` | композиция, `steps` |
| 4 | `RecipeBook` | `Recipe` | агрегация, `recipes` |
| 5 | `RecipeCategory` | `Recipe` | агрегация, `recipes` |
| 6 | `RecipeManager` | `Recipe` | агрегация, словарь рецептов |
| 7 | `Dish` (и наследники) | `Recipe` | поле `recipe`, `replace_recipe(recipe)` |
| 8 | `Soup` | `Ingredient` | `extra_components` |
| 9 | `Garnish` | `Ingredient` | `ingredients` (ингредиент, граммы) |
| 10 | `Sauce` | `Ingredient` | `base_ingredient` |
| 11 | `MainCourse` | `Garnish` | `side_dish` |
| 12 | `Salad` | `Sauce` | `dressing` |
| 13 | `Pastry` | `Oven` | параметр `can_bake_in(oven)` |
| 14 | `Portion` | `Dish` | поле `dish` |
| 15 | `Menu` | `Dish` | агрегация, `dishes` |
| 16 | `MenuItem` | `Dish` | поле `dish` |
| 17 | `Workstation` | `Person` | `assigned_worker` |
| 18 | `Workstation` | `KitchenTool` | `tools` |
| 19 | `Kitchen` | `Workstation` | `workstations` |
| 20 | `Kitchen` | `CookingEquipment` | `equipment` |
| 21 | `Kitchen` | `Recipe`, `Warehouse` | параметры `validate_recipe`, `cook_recipe` |
| 22 | `KitchenInventory` | `KitchenTool`, `CookingEquipment` | `tools`, `equipment` |
| 23 | `Refrigerator` | `Ingredient` | параметр `can_store(ingredient)` |
| 24 | `KitchenAssistant` | `KitchenTool` | параметр `prepare_work_area(tools)` |
| 25 | `Allergen` | `Recipe` | параметры `find_in_recipe`, `ensure_absent` |
| 26 | `DietPlan` | `Dish` | `meals` |
| 27 | `CalorieCalculator` | `Ingredient`, `Recipe` | параметры методов расчёта |
| 28 | `Customer` | `Allergen` | `allergies` |
| 29 | `Customer` | `Dish` | параметр `ensure_can_eat(dish)` |
| 30 | `Chef` | `ChefSpecialization` | `specialization` |
| 31 | `Chef` | `Recipe` | параметр `prepare_recipe(recipe, category)` |
| 32 | `Nutritionist` | `DietPlan` | параметр `review_plan(plan)` |
| 33 | `Order` | `Customer` | `customer` |
| 34 | `Order` | `OrderItem` | композиция, `items` |
| 35 | `OrderItem` | `Dish` | `dish` |
| 36 | `Payment` | `Order` / `Purchase` | `order` (любой объект с `calculate_total`) |
| 37 | `Receipt` | `Order`, `Payment` | `order`, `payment` |
| 38 | `CustomerOrder` | `Customer`, `Order` | `customer`, `order` |
| 39 | `Delivery` | `Order` | `order` |
| 40 | `StockItem` | `Ingredient` | `ingredient` |
| 41 | `Warehouse` | `StockItem` | композиция, `stock_items` |
| 42 | `Stock` | `StockItem` | `items` |
| 43 | `Supplier` | `Ingredient` | `products` |
| 44 | `Purchase` | `Supplier`, `Ingredient` | `supplier`, `ingredient` |
| 45 | `ProductBatch` | `Ingredient`, `Supplier` | `ingredient`, `supplier` |
| 46 | `SupplierDelivery` | `Supplier`, `ProductBatch` | `supplier`, `batches` |
| 47 | `Inventory` | `Warehouse`, `StockItem` | `warehouse`, `counted_items` |
| 48 | `InventoryManager` | `Warehouse` | `warehouse` |
| 49 | `ExpirationTracker` | `Ingredient` | `ingredients` |
| 50 | `CulinarySystem` | `Warehouse`, `Kitchen`, `RecipeManager`, `MenuItem`, `Order`, `Payment`, `Delivery`, `Purchase` | поля-репозитории |

**Наследование:** 9 продуктов → `Ingredient`; `Soup`, `Salad`, `Dessert`,
`Pastry`, `MainCourse`, `Beverage` → `Dish`; `Oven`, `Stove`, `Refrigerator`,
`Blender` → `CookingEquipment`; `FryingPan`, `Saucepan` → `KitchenTool`;
`Chef`, `Cook`, `Customer`, `KitchenWorker`, `KitchenAssistant`, `Nutritionist` → `Person`.
`Garnish` и `Sauce` — не блюда, а компоненты блюд (ассоциации 11–12).

## 7. Иерархия исключений

Единый корень — `CulinaryException`. Ветка `CulinaryError` (с сообщением по умолчанию)
наследуется от него; пять «Error»-классов дополнительно наследуют профильные
«Exception»-группы, поэтому их можно перехватывать любым из двух имён.

```text
CulinaryException
├── InvalidIngredientException ── InvalidIngredientError*
├── InsufficientStockException ── InsufficientIngredientError*
├── ExpiredProductException ───── ExpiredIngredientError*
├── InvalidRecipeException ────── InvalidRecipeStepError*
├── PaymentException ──────────── PaymentError*
├── CookingTimeException
├── InvalidTemperatureException
├── InvalidOrderException
├── AllergenException
├── PortionException
└── CulinaryError
    ├── RecipeNotFoundError
    ├── DishUnavailableError
    ├── KitchenEquipmentError
    │   └── UnavailableToolException
    ├── WarehouseCapacityError
    ├── SupplierError
    ├── OrderStateError
    └── * — также наследники CulinaryError
```

| Исключение | Когда возникает (примеры) |
|---|---|
| `InvalidIngredientError` | пустое название, неположительный вес, неизвестная единица измерения, некорректные параметры продукта |
| `InsufficientIngredientError` | не хватает ингредиента в партии/на складе, несовпадение партии с рецептом |
| `ExpiredIngredientError` | попытка использовать или принять просроченный продукт |
| `InvalidRecipeException` | дубликат рецепта, удаление рецепта, используемого в меню, смена названия при обновлении |
| `InvalidRecipeStepError` | неверный номер/описание/длительность шага, повтор номера |
| `RecipeNotFoundError` | рецепт не найден в `RecipeManager`/`RecipeBook` |
| `CookingTimeException` | отрицательное время в `Recipe`, `CookingTime`, `Pastry`, `Oven` |
| `InvalidTemperatureException` | температура хранения, подачи, шага, выпечки, духовки, холодильника, масла вне диапазона |
| `PortionException` | неверное число порций, вес порции/гарнира, масштабирование рецепта |
| `AllergenException` | блюдо содержит аллерген клиента или исключённый планом питания ингредиент |
| `DishUnavailableError` | блюдо отсутствует в меню, временно недоступно или уже добавлено |
| `KitchenEquipmentError` | неисправное оборудование, грязная кухня, занятое рабочее место, неразогретая духовка |
| `UnavailableToolException` | на рабочем месте есть грязный или повреждённый инструмент |
| `WarehouseCapacityError` | поступление превышает вместимость склада |
| `SupplierError` | поставщик не поставляет продукт, неверный рейтинг, нарушение статусов поставки |
| `InvalidOrderException` | пустой/дублирующийся заказ, цена позиции не совпадает с меню, доставка не найдена |
| `OrderStateError` | недопустимый переход статуса заказа, доставки или закупки |
| `PaymentError` | недостаточная сумма, неизвестный способ оплаты, повторная оплата, чек без оплаты |
| `CulinaryError` | шеф не допущен к категории блюда (общая ошибка домена) |

## 8. Рабочие сценарии (`CulinarySystem`)

1. **Склад:** добавление продукта, пополнение, удаление пустой позиции; контроль вместимости.
2. **Рецепты:** создание, изменение (новая версия автоматически подставляется в блюда меню),
   удаление (запрещено, если рецепт используется в меню).
3. **Меню:** добавление блюда (без дубликатов), включение/выключение доступности.
4. **Заказ:** создание с проверкой меню, цен и аллергенов клиента; редактирование до оплаты; отмена.
5. **Оплата:** наличные (со сдачей), карта/онлайн (только точная сумма); возврат возвращает
   только удержанную сумму.
6. **Приготовление:** только оплаченный новый заказ; проверяются чистота кухни, оборудование,
   инструменты, свежесть и суммарные остатки по всему заказу до первого списания.
7. **Выдача:** самовывоз (`hand_over_order`) или доставка: оплата доставки → «в пути» → «доставлен»
   → заказ «выдан».
8. **Закупка:** только у поставщика, в ассортименте которого есть продукт; оплата → приёмка на склад.

## 9. Консольный интерфейс

`python main.py` открывает меню `CulinaryConsole` (`cli/console.py`):

| Пункт | Действия |
|---|---|
| 1. Склад | остатки, добавить продукт, пополнить, удалить пустую позицию |
| 2. Рецепты | список, создать, изменить, удалить |
| 3. Меню блюд | список, добавить блюдо, доступность |
| 4. Заказы | список, создать, изменить, отменить, выдать (самовывоз) |
| 5. Приготовление | приготовить оплаченный заказ со списанием продуктов |
| 6. Оплата и возврат | оплата заказа, доставки, закупки; возврат оплаты |
| 7. Доставка | оформить, изменить статус |
| 8. Отчёт по складу | остатки, стоимость запасов, что нужно дозаказать |

Консоль только читает ввод, вызывает методы `CulinarySystem` и печатает результат.
Функции ввода и вывода передаются в конструктор (`read`, `write`), поэтому меню
покрыто автоматическими тестами (`tests/test_cli.py`).

## 10. Тестирование и CI/CD

- **Тесты:** `pytest`, 277 тестов; на каждый класс модели — свой `Test<ИмяКласса>`.
  Исключения и вспомогательные модули проверяются в `test_exceptions.py` и `test_validation.py`.
- **Покрытие:** строки + ветви по `culinary`, `cli` и `main` ≈ **99,8 %**;
  `pytest.ini` задаёт `--cov-fail-under=90`, поэтому падение ниже 90 % ломает сборку.
- **Пайплайн** `.github/workflows/laba2.yaml` (запуск при изменениях в `laba2/`):
  1. `lint` — `flake8` и `black --check`;
  2. `test` — pytest с покрытием на Python 3.11, 3.12 и 3.13, отчёт `coverage.xml` в артефактах;
  3. `build` — `python build.py`, пробный запуск `.pyz`, загрузка артефакта;
     при push в `main` артефакт публикуется в **Releases** (тег `lab2-build-<номер>`).

## 11. Качество кода

- Методы не длиннее ~20 строк, вложенность не больше 3 уровней, строки до 150 символов (`.flake8`).
- Числовые значения вынесены в именованные константы классов и `culinary/units.py`;
  статусы заказов, доставок, платежей и закупок — константы (`Order.NEW`, `Payment.PAID` …).
- Единый стиль форматирования обеспечивает `black` (длина строки 120).
