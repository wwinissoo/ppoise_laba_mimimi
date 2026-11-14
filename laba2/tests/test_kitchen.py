import pytest

from culinary.exceptions import (
    CookingTimeException,
    InsufficientIngredientError,
    InvalidTemperatureException,
    KitchenEquipmentError,
    UnavailableToolException,
)
from culinary.ingredients import Vegetable
from culinary.kitchen import (
    Blender,
    CookingEquipment,
    FryingPan,
    Kitchen,
    KitchenInventory,
    KitchenTool,
    Oven,
    Refrigerator,
    Saucepan,
    Stove,
    Workstation,
)
from culinary.people import Cook
from culinary.recipes import Recipe
from culinary.warehouse import StockItem, Warehouse


@pytest.fixture
def cook():
    return Cook("Иван", "+7 900 111-11-11", "", 30)


class TestKitchenTool:
    def test_lifecycle(self):
        knife = KitchenTool("Нож", "сталь")
        assert knife.name == "Нож" and knife.material == "сталь" and knife.condition == "исправен"
        knife.use()
        assert not knife.is_clean and not knife.is_usable()
        knife.clean()
        knife.mark_damaged()
        with pytest.raises(KitchenEquipmentError):
            knife.use()
        assert knife.repair() and knife.condition == "изношен" and knife.is_usable()
        assert not knife.repair()

    def test_validation(self):
        with pytest.raises(KitchenEquipmentError):
            KitchenTool("Нож", "сталь", "сломан")
        with pytest.raises(KitchenEquipmentError):
            KitchenTool(" ", "сталь")


class TestFryingPan:
    def test_behaviour(self):
        pan = FryingPan("Сковорода", "тефлон")
        assert pan.is_usable() and pan.diameter_cm == FryingPan.DEFAULT_DIAMETER_CM
        assert pan.suitable_for_portions(3) and not pan.suitable_for_portions(4)
        assert pan.recommend_heat() == "средний"
        assert FryingPan("Сковорода", "чугун").recommend_heat() == "средний или сильный"
        with pytest.raises(KitchenEquipmentError):
            FryingPan("Сковорода", "чугун", diameter_cm=0)


class TestSaucepan:
    def test_behaviour(self):
        pan = Saucepan("Кастрюля", "сталь", capacity_liters=4)
        assert pan.is_usable() and pan.capacity_liters == 4
        assert pan.can_hold(3) and not pan.can_hold(5)
        assert pan.fill_percentage(1) == 25
        with pytest.raises(ValueError):
            pan.fill_percentage(-1)
        with pytest.raises(KitchenEquipmentError):
            Saucepan("Кастрюля", "сталь", capacity_liters=0)


class TestCookingEquipment:
    def test_lifecycle(self):
        mixer = CookingEquipment("Миксер", 300)
        assert mixer.name == "Миксер" and mixer.power_watts == 300 and mixer.is_operational()
        mixer.turn_on()
        assert mixer.status == "включено"
        mixer.turn_off()
        mixer.pass_days(30)
        assert mixer.last_service_days == 30 and mixer.needs_service(30) and not mixer.needs_service(60)
        mixer.mark_broken()
        mixer.turn_off()
        assert mixer.status == "неисправно"
        with pytest.raises(KitchenEquipmentError):
            mixer.turn_on()
        mixer.record_service()
        assert mixer.status == "выключено" and mixer.last_service_days == 0

    def test_validation(self):
        with pytest.raises(KitchenEquipmentError):
            CookingEquipment("Миксер", -1)
        with pytest.raises(KitchenEquipmentError):
            CookingEquipment("Миксер", 100, "сломано")
        with pytest.raises(KitchenEquipmentError):
            CookingEquipment("Миксер", 100).pass_days(0)


class TestOven:
    def test_baking(self):
        oven = Oven("Духовка", 2000, "выключено", 0, 250)
        with pytest.raises(KitchenEquipmentError):
            oven.bake(10)
        with pytest.raises(InvalidTemperatureException):
            oven.preheat(300)
        assert oven.preheat(180) == 180 and oven.current_temperature == 180 and oven.max_temperature == 250
        assert oven.bake(30) == 30
        with pytest.raises(CookingTimeException):
            oven.bake(0)
        assert oven.estimate_energy_kwh(30) == pytest.approx(1)
        oven.turn_off()
        assert oven.current_temperature == 0

    def test_validation(self):
        with pytest.raises(KitchenEquipmentError):
            Oven("Духовка", 2000, "выключено", 0, 0)
        with pytest.raises(CookingTimeException):
            Oven("Духовка", 2000, "выключено", 0, 250).estimate_energy_kwh(-1)


class TestRefrigerator:
    def test_behaviour(self, tomato):
        fridge = Refrigerator("Холодильник", 200, "включено", 0, 4)
        assert fridge.can_store(tomato) and not fridge.is_freezing()
        fridge.set_temperature(-18)
        assert fridge.temperature == -18 and fridge.is_freezing() and not fridge.can_store(tomato)
        assert fridge.estimate_daily_energy() == pytest.approx(4.8)
        with pytest.raises(InvalidTemperatureException):
            fridge.set_temperature(25)
        with pytest.raises(InvalidTemperatureException):
            Refrigerator("Холодильник", 200, "включено", 0, 25)


class TestStove:
    def test_behaviour(self):
        stove = Stove("Плита", 3000)
        assert stove.burner_count == Stove.DEFAULT_BURNERS
        assert stove.can_use_burners(2) and not stove.can_use_burners(5)
        assert stove.estimate_energy(60) == 3
        stove.mark_broken()
        assert not stove.can_use_burners(1)
        with pytest.raises(KitchenEquipmentError):
            Stove("Плита", 3000, burner_count=0)


class TestBlender:
    def test_behaviour(self):
        blender = Blender("Блендер", 600)
        assert blender.max_speed == Blender.DEFAULT_MAX_SPEED
        assert blender.validate_speed(3) and not blender.validate_speed(True) and not blender.validate_speed(9)
        assert blender.blend_time(2) == 2 * Blender.SECONDS_PER_INGREDIENT
        with pytest.raises(KitchenEquipmentError):
            blender.blend_time(0)
        with pytest.raises(KitchenEquipmentError):
            Blender("Блендер", 600, max_speed=0)


class TestWorkstation:
    def test_booking(self, cook):
        other = Cook("Пётр", "+7 900 222-22-22", "", 30)
        station = Workstation(1)
        station.assign_worker(cook)
        station.assign_worker(cook)
        assert station.is_occupied and station.assigned_worker is cook and station.number == 1
        with pytest.raises(KitchenEquipmentError):
            station.assign_worker(other)
        station.release()
        station.assign_worker(other)
        assert station.assigned_worker is other
        with pytest.raises(TypeError):
            station.assign_worker("Пётр")

    def test_tools(self, cook):
        pan = FryingPan("Сковорода", "чугун")
        station = Workstation(2, cook, [pan, pan])
        assert station.tools == (pan,) and station.find_unusable_tools() == []
        pan.use()
        assert station.find_unusable_tools() == [pan]
        with pytest.raises(TypeError):
            station.add_tool("нож")

    def test_validation(self):
        with pytest.raises(KitchenEquipmentError):
            Workstation(0)
        with pytest.raises(KitchenEquipmentError):
            Workstation(1, is_occupied=True)


class TestKitchenInventory:
    def test_registry(self):
        inventory = KitchenInventory()
        oven = Oven("Духовка", 2000, "выключено", 0, 250)
        broken_pan = FryingPan("Сковорода", "чугун", condition="повреждён")
        inventory.register_equipment(oven)
        inventory.register_equipment(oven)
        inventory.register_tool(broken_pan)
        assert inventory.count_items() == 2 and inventory.tools == (broken_pan,) and inventory.equipment == (oven,)
        assert inventory.find_unavailable() == [broken_pan]
        oven.pass_days(100)
        assert inventory.find_needing_service(90) == [oven]
        with pytest.raises(TypeError):
            inventory.register_tool(oven)
        with pytest.raises(TypeError):
            inventory.register_equipment(broken_pan)


class TestKitchen:
    def test_cooking(self, recipe, tomato):
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1)], 10)
        dill = Vegetable("Укроп", 10, 500, 40, 5, 4)
        recipe.add_ingredient(dill, 50, is_optional=True)
        kitchen = Kitchen("Кухня", [Workstation(1, tools=[FryingPan("Сковорода", "чугун")])], [Stove("Плита", 3000)])
        assert kitchen.cook_recipe(recipe, warehouse)
        assert tomato.weight == 800 and warehouse.get_available_quantity(tomato) == pytest.approx(0.8)
        assert dill.weight == 10

    def test_optional_deduction_failure_is_ignored(self, recipe, tomato):
        dill = Vegetable("Укроп", 100, 500, 40, 5, 4)
        other_dill = Vegetable("Укроп", 100, 500, 40, 5, 4)
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1), StockItem(other_dill, 0.1)], 10)
        recipe.add_ingredient(dill, 50, is_optional=True)
        assert Kitchen("Кухня").cook_recipe(recipe, warehouse) and dill.weight == 100

    def test_stock_checks(self, recipe, tomato):
        kitchen = Kitchen("Кухня")
        with pytest.raises(InsufficientIngredientError):
            kitchen.validate_recipe(recipe, Warehouse("Склад", ""))
        lookalike = Vegetable("Помидор", 1000, 200, 18, 7, 4)
        with pytest.raises(InsufficientIngredientError):
            kitchen.validate_recipe(recipe, Warehouse("Склад", "", [StockItem(lookalike, 1)]))
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1)])
        with pytest.raises(InsufficientIngredientError):
            kitchen.validate_recipe(recipe, warehouse, 10)
        with pytest.raises(ValueError):
            kitchen.validate_recipe(recipe, warehouse, 0)
        greedy = Recipe("Много", "", 1, 1)
        greedy.add_ingredient(tomato, 1.5, "кг")
        tomato.receive(1000)
        with pytest.raises(InsufficientIngredientError):
            kitchen.validate_recipe(greedy, warehouse)

    def test_readiness(self):
        pan = FryingPan("Сковорода", "чугун")
        kitchen = Kitchen("Кухня", [Workstation(1, tools=[pan])], [Stove("Плита", 3000)])
        assert kitchen.check_readiness()
        pan.use()
        with pytest.raises(UnavailableToolException):
            kitchen.check_readiness()
        pan.clean()
        kitchen.soil(30)
        assert kitchen.cleanliness_level == 70 and not kitchen.is_clean()
        with pytest.raises(KitchenEquipmentError):
            kitchen.check_readiness()
        kitchen.record_cleaning()
        kitchen.equipment[0].mark_broken()
        with pytest.raises(KitchenEquipmentError):
            kitchen.check_readiness()

    def test_workstations(self, cook):
        kitchen = Kitchen("Кухня", [Workstation(1, cook), Workstation(2)])
        assert kitchen.name == "Кухня" and kitchen.find_free_workstation().number == 2
        assert Kitchen("Пустая").find_free_workstation() is None
        with pytest.raises(KitchenEquipmentError):
            kitchen.add_workstation(Workstation(1))
        with pytest.raises(AttributeError):
            kitchen.workstations.append(Workstation(3))
        with pytest.raises(TypeError):
            kitchen.add_workstation("стол")
        with pytest.raises(TypeError):
            kitchen.register_equipment("плита")

    def test_validation(self):
        with pytest.raises(KitchenEquipmentError):
            Kitchen("Кухня", cleanliness_level=150)
        with pytest.raises(KitchenEquipmentError):
            Kitchen("Кухня").soil(0)
