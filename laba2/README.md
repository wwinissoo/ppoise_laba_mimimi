# Lab 2: "Culinary" (Culinary System)

## 1. Purpose

An object model of a restaurant kitchen: ingredient and warehouse accounting, recipes and
technological cards, dishes and menus, kitchen equipment, staff, nutrition values and allergens,
customer orders, payment, receipts and delivery.
The domain (`culinary/`) is completely separated from the console interface (`cli/`);
all state is kept in memory for the current run.

## 2. Build, run and test (console only, no IDE)

```bash
cd laba2
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt   # pytest, pytest-cov, flake8, black

.venv/bin/python main.py                         # console menu
.venv/bin/python -m pytest                       # tests + coverage (90 % threshold)
.venv/bin/flake8 .                               # static analysis
.venv/bin/black --check culinary cli main.py build.py tests   # consistent style
.venv/bin/python build.py                        # artifact dist/culinary-lab2.pyz
python3 dist/culinary-lab2.pyz                   # run the built artifact
```

The `culinary-lab2.pyz` artifact is a self-contained Python zip archive (`zipapp` module):
running it needs only Python 3.11+, with no dependency installation and no sources.

## 3. Project structure

```text
laba2/
├── culinary/                # the domain (knows nothing about the console)
│   ├── application.py       # CulinarySystem — business-process facade
│   ├── validation.py        # shared input and status-transition checks
│   ├── units.py             # units of measurement and conversion factors
│   ├── ingredients/         # Ingredient and 9 kinds of products
│   ├── recipes/             # Recipe, RecipeIngredient, steps, books, categories
│   ├── dishes/              # Dish and subclasses, garnish, sauce, portion, menu
│   ├── kitchen/             # Kitchen, equipment, tools, workstations
│   ├── nutrition/           # allergens, nutrients, nutrition facts, diet plan
│   ├── people/              # Person and subclasses, chef specialization
│   ├── orders/              # Order, OrderItem, Payment, Receipt, Delivery
│   ├── warehouse/           # Warehouse, StockItem, suppliers, purchases, batches
│   └── exceptions/          # custom exception hierarchy
├── cli/console.py           # CulinaryConsole — menu, input/output only
├── main.py                  # entry point
├── build.py                 # executable artifact build
├── tests/                   # pytest: a separate Test class for every model class
├── pytest.ini               # runs tests with coverage and a 90 % threshold
├── pyproject.toml, .flake8  # black, coverage and flake8 settings
├── requirements.txt         # test dependencies
└── requirements-dev.txt     # + linters
```

CI/CD pipelines: `.github/workflows/` in the repository root (section 10).

## 4. Compliance with the quantitative requirements

| Requirement | Minimum | Actual |
|---|---|---|
| Classes | 50 | **96** (72 domain classes + 24 exceptions) |
| Fields (total, exceptions excluded) | 150 | **245** |
| Unique behaviours (methods that are not getters/setters) | 100 | **293** unique by name, 317 in total |
| Associations between classes | 30 | **50** (see section 6) |
| Custom exceptions | 12 | **24** (see section 7) |

The aliases `NutritionValue = Nutrient`, `DietaryPlan = DietPlan`,
`culinary.orders.Menu/MenuItem` and `culinary.warehouse.Delivery = SupplierDelivery`
are kept only for import compatibility and are **not counted** as separate classes.

All fields are stored in private attributes (`self.__field`) and exposed through
read-only properties; collections are returned as tuples (`tuple`), so they can
only be changed through class methods that validate their input.

## 5. Classes, fields and methods

The tables list the fields (initialised in `__init__`, exposed through properties)
and the methods with domain behaviour. Property getters are not listed.

### 5.1. Ingredients (`culinary.ingredients`)

| Class | Parent | Fields | Methods (behaviour) |
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

### 5.2. Recipes (`culinary.recipes`)

| Class | Parent | Fields | Methods (behaviour) |
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

### 5.3. Dishes (`culinary.dishes`)

| Class | Parent | Fields | Methods (behaviour) |
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

### 5.4. Kitchen (`culinary.kitchen`)

| Class | Parent | Fields | Methods (behaviour) |
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

### 5.5. Nutrition (`culinary.nutrition`)

| Class | Parent | Fields | Methods (behaviour) |
|---|---|---|---|
| `Allergen` | — | name, severity, description | `matches_ingredient`, `find_in_recipe`, `ensure_absent`, `describe` |
| `CalorieCalculator` | — | — | `calculate_ingredient`, `calculate_recipe`, `calculate_per_serving`, `calculate_daily_balance` |
| `DietPlan` | — | title, excluded_ingredients, daily_calorie_limit, meals | `is_ingredient_allowed`, `is_dish_allowed`, `add_meal`, `calculate_daily_calories`, `is_within_limit`, `remaining_calories` |
| `Nutrient` | — | name, amount_grams, daily_value_grams, unit | `daily_value_percentage`, `is_deficient`, `convert_to_milligrams`, `amount_in_display_unit` |
| `NutritionFacts` | — | calories, protein, fat, carbohydrates, serving_grams | `calculate_energy_from_macros`, `scale_to_serving`, `is_high_protein` |

### 5.6. People (`culinary.people`)

| Class | Parent | Fields | Methods (behaviour) |
|---|---|---|---|
| `Chef` | Person | specialization, experience_years | `is_qualified`, `can_prepare`, `prepare_recipe`, `add_experience` |
| `ChefSpecialization` | — | title, allowed_categories, certification_level, years_required | `allows`, `is_certified`, `experience_requirement_met` |
| `Cook` | Person | shift_hours, skill_level | `estimate_shift_end`, `improve_skill` |
| `Customer` | Person | loyalty_points, allergies | `add_loyalty_points`, `spend_loyalty_points`, `earn_points_for_purchase`, `add_allergy`, `ensure_can_eat` |
| `KitchenAssistant` | Person | assigned_area | `change_area`, `prepare_work_area`, `count_unclean_tools` |
| `KitchenWorker` | Person | position, shift_hours | `change_position`, `extend_shift`, `finish_shift` |
| `Nutritionist` | Person | qualification, experience_years | `review_plan`, `add_experience` |
| `Person` | — | name, phone, email, age | `change_phone`, `has_valid_contact`, `is_adult` |

### 5.7. Orders (`culinary.orders`)

| Class | Parent | Fields | Methods (behaviour) |
|---|---|---|---|
| `CustomerOrder` | — | customer, order, delivery_address, delivery_required | `request_delivery`, `cancel_delivery`, `get_customer_name` |
| `Delivery` | — | order, address, delivery_fee, status | `calculate_total`, `update_status`, `is_completed`, `is_cancelled` |
| `Order` | — | order_number, customer, items, status, created_at | `add_item`, `remove_item`, `replace_items`, `calculate_total`, `count_portions`, `change_status` |
| `OrderItem` | — | dish, quantity, unit_price, note | `calculate_total`, `increase_quantity`, `update_quantity`, `update_unit_price`, `add_note` |
| `Payment` | — | order, amount, method, status, purpose, expected_amount, charged_amount | `process`, `refund`, `is_paid`, `is_refunded` |
| `Receipt` | — | order, payment, receipt_number, issued | `issue`, `format_total`, `format_lines`, `void` |

### 5.8. Warehouse (`culinary.warehouse`)

| Class | Parent | Fields | Methods (behaviour) |
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

### 5.9. Facade (`culinary.application`)

| Class | Parent | Fields | Methods (behaviour) |
|---|---|---|---|
| `CulinarySystem` | — | warehouse, kitchen, recipe_manager, menu_items, orders, order_payments, delivery_payments, deliveries, purchase_payments, ingredients | `register_ingredient`, `add_ingredient`, `get_ingredient`, `restock_ingredient`, `delete_ingredient`, `add_recipe`, `update_recipe`, `delete_recipe`, `add_menu_item`, `set_dish_availability`, `create_order_item`, `create_order`, `get_order`, `edit_order`, `pay_order`, `refund_order`, `cancel_order`, `pay_purchase`, `receive_purchase`, `pay_delivery`, `cook_order`, `hand_over_order`, `create_delivery`, `update_delivery_status` |


## 6. Associations between classes

An association means a class stores another class in a field or accepts it as a method parameter.
The types of associated objects are checked with `isinstance`.

| # | Class | Linked with | Kind |
|---|---|---|---|
| 1 | `RecipeIngredient` | `Ingredient` | field `ingredient` |
| 2 | `Recipe` | `RecipeIngredient` | composition, `ingredients` |
| 3 | `Recipe` | `RecipeStep` | composition, `steps` |
| 4 | `RecipeBook` | `Recipe` | aggregation, `recipes` |
| 5 | `RecipeCategory` | `Recipe` | aggregation, `recipes` |
| 6 | `RecipeManager` | `Recipe` | aggregation, recipe dictionary |
| 7 | `Dish` (and subclasses) | `Recipe` | field `recipe`, `replace_recipe(recipe)` |
| 8 | `Soup` | `Ingredient` | `extra_components` |
| 9 | `Garnish` | `Ingredient` | `ingredients` (ingredient, grams) |
| 10 | `Sauce` | `Ingredient` | `base_ingredient` |
| 11 | `MainCourse` | `Garnish` | `side_dish` |
| 12 | `Salad` | `Sauce` | `dressing` |
| 13 | `Pastry` | `Oven` | parameter of `can_bake_in(oven)` |
| 14 | `Portion` | `Dish` | field `dish` |
| 15 | `Menu` | `Dish` | aggregation, `dishes` |
| 16 | `MenuItem` | `Dish` | field `dish` |
| 17 | `Workstation` | `Person` | `assigned_worker` |
| 18 | `Workstation` | `KitchenTool` | `tools` |
| 19 | `Kitchen` | `Workstation` | `workstations` |
| 20 | `Kitchen` | `CookingEquipment` | `equipment` |
| 21 | `Kitchen` | `Recipe`, `Warehouse` | parameters of `validate_recipe`, `cook_recipe` |
| 22 | `KitchenInventory` | `KitchenTool`, `CookingEquipment` | `tools`, `equipment` |
| 23 | `Refrigerator` | `Ingredient` | parameter of `can_store(ingredient)` |
| 24 | `KitchenAssistant` | `KitchenTool` | parameter of `prepare_work_area(tools)` |
| 25 | `Allergen` | `Recipe` | parameters of `find_in_recipe`, `ensure_absent` |
| 26 | `DietPlan` | `Dish` | `meals` |
| 27 | `CalorieCalculator` | `Ingredient`, `Recipe` | parameters of the calculation methods |
| 28 | `Customer` | `Allergen` | `allergies` |
| 29 | `Customer` | `Dish` | parameter of `ensure_can_eat(dish)` |
| 30 | `Chef` | `ChefSpecialization` | `specialization` |
| 31 | `Chef` | `Recipe` | parameter of `prepare_recipe(recipe, category)` |
| 32 | `Nutritionist` | `DietPlan` | parameter of `review_plan(plan)` |
| 33 | `Order` | `Customer` | `customer` |
| 34 | `Order` | `OrderItem` | composition, `items` |
| 35 | `OrderItem` | `Dish` | `dish` |
| 36 | `Payment` | `Order` / `Purchase` | `order` (any object with `calculate_total`) |
| 37 | `Receipt` | `Order`, `Payment` | `order`, `payment` |
| 38 | `CustomerOrder` | `Customer`, `Order` | `customer`, `order` |
| 39 | `Delivery` | `Order` | `order` |
| 40 | `StockItem` | `Ingredient` | `ingredient` |
| 41 | `Warehouse` | `StockItem` | composition, `stock_items` |
| 42 | `Stock` | `StockItem` | `items` |
| 43 | `Supplier` | `Ingredient` | `products` |
| 44 | `Purchase` | `Supplier`, `Ingredient` | `supplier`, `ingredient` |
| 45 | `ProductBatch` | `Ingredient`, `Supplier` | `ingredient`, `supplier` |
| 46 | `SupplierDelivery` | `Supplier`, `ProductBatch` | `supplier`, `batches` |
| 47 | `Inventory` | `Warehouse`, `StockItem` | `warehouse`, `counted_items` |
| 48 | `InventoryManager` | `Warehouse` | `warehouse` |
| 49 | `ExpirationTracker` | `Ingredient` | `ingredients` |
| 50 | `CulinarySystem` | `Warehouse`, `Kitchen`, `RecipeManager`, `MenuItem`, `Order`, `Payment`, `Delivery`, `Purchase` | repository fields |

**Inheritance:** 9 products → `Ingredient`; `Soup`, `Salad`, `Dessert`,
`Pastry`, `MainCourse`, `Beverage` → `Dish`; `Oven`, `Stove`, `Refrigerator`,
`Blender` → `CookingEquipment`; `FryingPan`, `Saucepan` → `KitchenTool`;
`Chef`, `Cook`, `Customer`, `KitchenWorker`, `KitchenAssistant`, `Nutritionist` → `Person`.
`Garnish` and `Sauce` are not dishes but dish components (associations 11–12).

## 7. Exception hierarchy

There is a single root, `CulinaryException`. The `CulinaryError` branch (with a default message)
inherits from it; five "Error" classes additionally inherit the matching
"Exception" groups, so they can be caught under either name.

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
    └── * — also subclasses of CulinaryError
```

| Exception | Raised when (examples) |
|---|---|
| `InvalidIngredientError` | empty name, non-positive weight, unknown unit of measurement, invalid product parameters |
| `InsufficientIngredientError` | not enough ingredient in the batch/warehouse, batch does not match the recipe |
| `ExpiredIngredientError` | an attempt to use or accept an expired product |
| `InvalidRecipeException` | duplicate recipe, deleting a recipe used in the menu, renaming on update |
| `InvalidRecipeStepError` | wrong step number/description/duration, repeated number |
| `RecipeNotFoundError` | recipe not found in `RecipeManager`/`RecipeBook` |
| `CookingTimeException` | negative time in `Recipe`, `CookingTime`, `Pastry`, `Oven` |
| `InvalidTemperatureException` | storage, serving, step, baking, oven, refrigerator or oil temperature out of range |
| `PortionException` | wrong number of portions, portion/garnish weight, recipe scaling |
| `AllergenException` | a dish contains a customer's allergen or an ingredient excluded by the diet plan |
| `DishUnavailableError` | dish is missing from the menu, temporarily unavailable or already added |
| `KitchenEquipmentError` | broken equipment, dirty kitchen, occupied workstation, oven not preheated |
| `UnavailableToolException` | a dirty or damaged tool at a workstation |
| `WarehouseCapacityError` | an arrival exceeds the warehouse capacity |
| `SupplierError` | supplier does not supply the product, wrong rating, delivery status violations |
| `InvalidOrderException` | empty/duplicate order, item price differs from the menu, delivery not found |
| `OrderStateError` | invalid status transition of an order, delivery or purchase |
| `PaymentError` | insufficient amount, unknown payment method, repeated payment, receipt without payment |
| `CulinaryError` | the chef is not allowed to cook the dish category (general domain error) |

## 8. Working scenarios (`CulinarySystem`)

1. **Warehouse:** add a product, restock, delete an empty position; capacity control.
2. **Recipes:** create, update (the new version is automatically substituted into menu dishes),
   delete (forbidden while the recipe is used in the menu).
3. **Menu:** add a dish (no duplicates), turn availability on/off.
4. **Order:** creation with menu, price and customer-allergen checks; editing until payment; cancellation.
5. **Payment:** cash (with change), card/online (exact amount only); a refund returns
   only the amount actually charged.
6. **Cooking:** only a paid new order; kitchen cleanliness, equipment, tools, freshness and the
   total stock for the whole order are checked before the first deduction.
7. **Handover:** pickup (`hand_over_order`) or delivery: delivery payment → "in transit" → "delivered"
   → order "handed over".
8. **Purchase:** only from a supplier whose assortment includes the product; payment → receipt into the warehouse.

## 9. Console interface

`python main.py` opens the `CulinaryConsole` menu (`cli/console.py`):

| Item | Actions |
|---|---|
| 1. Warehouse | stock, add product, restock, delete an empty position |
| 2. Recipes | list, create, update, delete |
| 3. Dish menu | list, add dish, availability |
| 4. Orders | list, create, edit, cancel, hand over (pickup) |
| 5. Cooking | cook a paid order, deducting products |
| 6. Payment and refund | pay for an order, delivery or purchase; refund an order payment |
| 7. Delivery | create, change status |
| 8. Warehouse report | stock, stock value, what needs to be reordered |

The console only reads input, calls `CulinarySystem` methods and prints the result.
The input and output functions are passed to the constructor (`read`, `write`), so the menu
is covered by automated tests (`tests/test_cli.py`).

## 10. Testing and CI/CD

- **Tests:** `pytest`, 278 tests; every model class has its own `Test<ClassName>`.
  Exceptions and helper modules are checked in `test_exceptions.py` and `test_validation.py`.
- **Coverage:** lines + branches over `culinary`, `cli` and `main`, about **99.8 %**;
  `pytest.ini` sets `--cov-fail-under=90`, so coverage below 90 % fails the build.
- **Pipelines** (`.github/workflows/`):
  1. `laba2.yaml` (runs on changes in `laba2/`): `lint` — `flake8` and `black --check`;
     `test` — pytest with coverage on Python 3.11, 3.12 and 3.13, `coverage.xml` is saved as an artifact;
  2. `build.yaml` (lab1 + lab2, on push to `main`): `python build.py`, a smoke run of the `.pyz`,
     artifact upload; both artifacts are published to **Releases** (tag `build-<number>`).

## 11. Code quality

- Methods are at most ~20 lines long, nesting is at most 3 levels, lines are up to 150 characters (`.flake8`).
- Numeric values are named class constants or live in `culinary/units.py`;
  order, delivery, payment and purchase statuses are constants (`Order.NEW`, `Payment.PAID` …).
- A uniform formatting style is enforced by `black` (line length 120).
