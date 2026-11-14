import pytest

from culinary.exceptions import (
    CulinaryException,
    ExpiredIngredientError,
    ExpiredProductException,
    InsufficientIngredientError,
    InsufficientStockException,
    InvalidIngredientError,
    InvalidTemperatureException,
)
from culinary.ingredients import DairyProduct, Egg, Fish, Flour, Fruit, Ingredient, Meat, Oil, Spice, Vegetable

BASE = ("Продукт", 1000, 100, 50, 10, 4)


def make(**overrides):
    params = dict(name="Соль", weight=500, price_per_kg=40, calories=0, expiration_days=30, storage_temperature=20)
    params.update(overrides)
    return Ingredient(**params)


class TestIngredient:
    @pytest.mark.parametrize(
        "field, value",
        [
            ("name", "  "),
            ("weight", 0),
            ("weight", -1),
            ("weight", True),
            ("price_per_kg", -1),
            ("calories", -5),
            ("expiration_days", 0),
            ("expiration_days", True),
            ("storage_temperature", "холод"),
        ],
    )
    def test_invalid_data(self, field, value):
        with pytest.raises(InvalidIngredientError):
            make(**{field: value})

    def test_zero_weight_allowed_for_catalog_card(self):
        card = make(weight=0, allow_zero=True)
        assert not card.is_available and card.calculate_remaining_percentage() == 0

    def test_storage_temperature_range(self):
        with pytest.raises(InvalidTemperatureException):
            make(storage_temperature=100)
        salt = make()
        salt.update_storage_temperature(-18)
        assert salt.storage_temperature == -18

    def test_properties(self):
        salt = make()
        assert (salt.name, salt.price_per_kg, salt.calories, salt.expiration_days) == ("Соль", 40, 0, 30)
        assert salt.initial_weight == 500 and salt.days_passed == 0

    def test_cost_does_not_depend_on_stock(self):
        assert make(weight=100).calculate_cost(1000) == pytest.approx(40)
        with pytest.raises(InvalidIngredientError):
            make().calculate_cost(0)

    def test_calories(self):
        assert make(calories=200).calculate_calories(50) == 100
        with pytest.raises(InvalidIngredientError):
            make().calculate_calories(-1)

    def test_consume_and_receive(self):
        salt = make()
        salt.consume(250)
        assert salt.calculate_remaining_percentage() == 50
        salt.consume(250)
        assert not salt.is_available
        salt.receive(200)
        assert salt.is_available and salt.weight == 200
        with pytest.raises(InsufficientIngredientError):
            salt.consume(1000)
        with pytest.raises(InvalidIngredientError):
            salt.receive(-5)

    def test_receive_sets_initial_weight_of_empty_card(self):
        card = make(weight=0, allow_zero=True)
        card.receive(300)
        assert card.initial_weight == 300

    def test_expiration_flow(self):
        salt = make(expiration_days=2)
        salt.pass_day()
        assert salt.require_fresh() and salt.is_available
        salt.pass_day()
        assert not salt.is_available and not salt.check_expiration()
        with pytest.raises(ExpiredIngredientError):
            salt.receive(10)

    def test_update_price(self):
        salt = make()
        salt.update_price(55)
        assert salt.price_per_kg == 55
        with pytest.raises(InvalidIngredientError):
            salt.update_price(-1)

    def test_exception_hierarchy_is_unified(self):
        assert issubclass(InvalidIngredientError, CulinaryException)
        assert issubclass(ExpiredIngredientError, ExpiredProductException)
        assert issubclass(InsufficientIngredientError, InsufficientStockException)


class TestVegetable:
    def test_processing(self):
        carrot = Vegetable(*BASE, is_organic=True, requires_peeling=True)
        assert carrot.is_organic and carrot.water_percentage == Vegetable.DEFAULT_WATER_PERCENTAGE
        assert not carrot.is_suitable_for_salad()
        assert carrot.wash() == "Продукт" and carrot.is_washed and carrot.is_suitable_for_salad()
        assert carrot.peel() and carrot.is_peeled
        assert carrot.calculate_clean_weight(10) == 900

    def test_rules(self):
        assert not Vegetable(*BASE).peel()
        with pytest.raises(InvalidIngredientError):
            Vegetable(*BASE, water_percentage=120)
        with pytest.raises(InvalidIngredientError):
            Vegetable(*BASE).calculate_clean_weight(100)


class TestFruit:
    def test_processing(self):
        mango = Fruit(*BASE, sweetness=8, is_ripe=False)
        with pytest.raises(InvalidIngredientError):
            mango.cut()
        assert mango.ripen() and mango.is_ripe
        assert mango.cut() == 1000 and mango.is_cut
        assert mango.calculate_sweetness_score() == 80
        assert mango.has_seeds and mango.remove_seeds() and not mango.has_seeds
        assert mango.sweetness == 8

    def test_invalid_sweetness(self):
        with pytest.raises(InvalidIngredientError):
            Fruit(*BASE, sweetness=11)


class TestMeat:
    def test_processing(self):
        beef = Meat(*BASE, fat_percentage=15, is_frozen=True)
        assert beef.meat_type == "говядина" and beef.is_frozen
        assert beef.defrost() is False and not beef.is_frozen
        assert beef.marinate("  соевый  ") == "соевый" and beef.is_marinated
        assert beef.calculate_fat_weight() == 150
        assert beef.check_fat_content(20) and not beef.check_fat_content(10)
        assert beef.fat_percentage == 15

    def test_rules(self):
        with pytest.raises(InvalidIngredientError):
            Meat(*BASE, fat_percentage=-1)
        with pytest.raises(InvalidIngredientError):
            Meat(*BASE).marinate(" ")


class TestFish:
    def test_cleaning(self):
        cod = Fish(*BASE, bone_count=12)
        assert cod.fish_type == "белая рыба" and cod.has_scales and not cod.is_cleaned
        assert not cod.is_ready_for_cooking()
        assert cod.remove_bones(2) == 10
        assert cod.clean_fish() and cod.bone_count == 0 and not cod.has_scales
        assert cod.is_ready_for_cooking()

    def test_rules(self):
        with pytest.raises(InvalidIngredientError):
            Fish(*BASE, bone_count=-1)
        with pytest.raises(InvalidIngredientError):
            Fish(*BASE, bone_count=3).remove_bones(5)


class TestDairyProduct:
    def test_fermentation(self):
        kefir = DairyProduct(*BASE, fermentation_required=True, lactose_free=True)
        assert not kefir.check_fermentation() and kefir.fermentation_required
        assert kefir.ferment(12) == 12 and kefir.is_fermented and kefir.check_fermentation()
        assert kefir.is_suitable_for_lactose_free_diet() and kefir.lactose_free
        assert kefir.calculate_fat_weight() == pytest.approx(32)
        assert kefir.fat_percentage == DairyProduct.DEFAULT_FAT_PERCENTAGE

    def test_rules(self):
        milk = DairyProduct(*BASE)
        assert milk.ferment(5) is False and milk.check_fermentation()
        with pytest.raises(InvalidIngredientError):
            milk.ferment(0)
        with pytest.raises(InvalidIngredientError):
            DairyProduct(*BASE, fat_percentage=101)


class TestSpice:
    def test_behaviour(self):
        pepper = Spice(*BASE, intensity=8)
        assert pepper.grind() and pepper.is_ground
        assert pepper.mix_with(Spice(*BASE, intensity=2)) == 5 and pepper.is_mixed
        pepper.adjust_intensity(3)
        assert pepper.intensity == 3 and pepper.describe_flavor() == "пряный, интенсивность 3/10"
        assert pepper.flavor == "пряный"

    def test_rules(self):
        with pytest.raises(InvalidIngredientError):
            Spice(*BASE, intensity=11)
        with pytest.raises(InvalidIngredientError):
            Spice(*BASE).adjust_intensity(-1)
        with pytest.raises(TypeError):
            Spice(*BASE).mix_with(make())


class TestFlour:
    def test_behaviour(self):
        flour = Flour(*BASE, gluten_content="высокое")
        assert flour.sift() == 1000 and flour.is_sifted
        assert flour.calculate_protein_weight() == 100
        assert flour.is_suitable_for_bread() and not Flour(*BASE, gluten_content="низкое").is_suitable_for_bread()
        flour.change_flour_type(" ржаная ")
        assert flour.flour_type == "ржаная" and flour.gluten_content == "высокое" and flour.protein_percentage == 10

    def test_rules(self):
        with pytest.raises(InvalidIngredientError):
            Flour(*BASE, protein_percentage=-5)
        with pytest.raises(InvalidIngredientError):
            Flour(*BASE).change_flour_type("")


class TestOil:
    def test_behaviour(self):
        oil = Oil(*BASE, smoke_point=180, is_refined=False)
        assert oil.heat(170) == 170 and oil.is_heated
        assert oil.is_suitable_for_frying(160) and not oil.is_suitable_for_frying(200)
        assert oil.calculate_remaining_after_frying(100) == 900
        assert oil.classify_refinement() == "нерафинированное"
        assert Oil(*BASE).classify_refinement() == "рафинированное"
        assert oil.smoke_point == 180 and not oil.is_refined and oil.oil_type == "растительное"

    def test_rules(self):
        with pytest.raises(InvalidIngredientError):
            Oil(*BASE, smoke_point=0)
        with pytest.raises(InvalidTemperatureException):
            Oil(*BASE).heat(250)
        with pytest.raises(InvalidIngredientError):
            Oil(*BASE).calculate_remaining_after_frying(5000)


class TestEgg:
    def test_behaviour(self):
        egg = Egg(*BASE, egg_size="L")
        assert egg.check_shell() and egg.is_suitable_for_boiling()
        assert egg.crack() == 1000 and egg.is_cracked and not egg.shell_intact
        assert not egg.is_suitable_for_boiling()
        egg.change_yolk_color_label(" оранжевый ")
        assert egg.yolk_color == "оранжевый" and egg.egg_size == "L"

    def test_rules(self):
        with pytest.raises(InvalidIngredientError):
            Egg(*BASE, egg_size="XXL")
        egg = Egg(*BASE, shell_intact=False)
        with pytest.raises(InvalidIngredientError):
            egg.crack()
        with pytest.raises(InvalidIngredientError):
            egg.change_yolk_color_label("")
