import pytest

from culinary.exceptions import AllergenException, CulinaryError
from culinary.nutrition import Allergen, DietPlan
from culinary.people import (
    Chef,
    ChefSpecialization,
    Cook,
    Customer,
    KitchenAssistant,
    KitchenWorker,
    Nutritionist,
    Person,
)
from culinary.kitchen import FryingPan

PHONE = "+7 900 000-00-00"


class TestPerson:
    def test_contacts(self):
        person = Person(" Анна ", PHONE, "anna@example.com", 18)
        assert person.name == "Анна" and person.email == "anna@example.com" and person.age == 18
        assert person.is_adult() and person.has_valid_contact()
        person.change_phone("")
        assert person.phone == "" and not Person("Боря", PHONE, "", 10).is_adult()

    @pytest.mark.parametrize(
        "phone, email, age", [("", "", 20), ("abc", "", 20), ("", "не-почта", 20), (PHONE, "", -1), (PHONE, "", True)]
    )
    def test_validation(self, phone, email, age):
        with pytest.raises(ValueError):
            Person("Анна", phone, email, age)

    def test_cannot_remove_last_contact(self):
        with pytest.raises(ValueError):
            Person("Анна", PHONE, "", 20).change_phone("")


class TestCustomer:
    def test_loyalty(self):
        customer = Customer("Анна", PHONE, "", 20, 10)
        customer.add_loyalty_points(5)
        customer.spend_loyalty_points(3)
        assert customer.loyalty_points == 12 and customer.earn_points_for_purchase(1000) == 50
        with pytest.raises(ValueError):
            customer.spend_loyalty_points(1000)
        with pytest.raises(ValueError):
            customer.add_loyalty_points(-1)
        with pytest.raises(ValueError):
            Customer("Анна", PHONE, "", 20, -5)

    def test_allergies(self, dish):
        customer = Customer("Анна", PHONE, "", 20, allergies=[Allergen("орехи"), Allergen("ОРЕХИ")])
        assert len(customer.allergies) == 1 and customer.ensure_can_eat(dish)
        customer.add_allergy(Allergen("помидор"))
        with pytest.raises(AllergenException):
            customer.ensure_can_eat(dish)
        with pytest.raises(TypeError):
            customer.add_allergy("орехи")


class TestChefSpecialization:
    def test_rules(self):
        pastry = ChefSpecialization("Кондитер", ["Десерты", "выпечка"], 2, 3)
        assert pastry.title == "Кондитер" and pastry.allowed_categories == ("выпечка", "десерты")
        assert pastry.allows(" ДЕСЕРТЫ ") and not pastry.allows("супы")
        assert pastry.is_certified() and pastry.certification_level == 2 and pastry.years_required == 3
        assert pastry.experience_requirement_met(3) and not pastry.experience_requirement_met(2)
        assert not ChefSpecialization("Стажёр", ["салаты"]).is_certified()

    @pytest.mark.parametrize("categories, level, years", [([], 0, 0), (["супы"], 9, 0), (["супы"], 0, -1)])
    def test_validation(self, categories, level, years):
        with pytest.raises(ValueError):
            ChefSpecialization("X", categories, level, years)


class TestChef:
    def test_qualification(self, recipe):
        pastry = ChefSpecialization("Кондитер", ["десерты"], 2, 3)
        junior = Chef("Олег", PHONE, "", 25, pastry, 1)
        assert not junior.is_qualified() and not junior.can_prepare("десерты")
        with pytest.raises(CulinaryError):
            junior.prepare_recipe(recipe, "десерты")
        junior.add_experience(2)
        assert junior.experience_years == 3 and junior.specialization is pastry
        assert junior.prepare_recipe(recipe, "десерты") == pytest.approx(40)
        with pytest.raises(TypeError):
            junior.prepare_recipe("рецепт", "десерты")
        with pytest.raises(ValueError):
            junior.add_experience(-1)

    def test_validation(self):
        with pytest.raises(TypeError):
            Chef("Олег", PHONE, "", 25, "кондитер", 1)
        with pytest.raises(ValueError):
            Chef("Олег", PHONE, "", 25, ChefSpecialization("Кондитер", ["десерты"]), -1)


class TestCook:
    def test_shift_and_skills(self):
        cook = Cook("Иван", PHONE, "", 30, shift_hours=10)
        assert cook.shift_hours == 10 and cook.estimate_shift_end(20) == 6
        for level in Cook.SKILL_LEVELS[1:]:
            assert cook.improve_skill() == level
        assert cook.skill_level == "мастер"
        with pytest.raises(ValueError):
            cook.improve_skill()
        with pytest.raises(ValueError):
            cook.estimate_shift_end(24)

    @pytest.mark.parametrize("hours, level", [(0, "начальный"), (25, "начальный"), (8, "гуру")])
    def test_validation(self, hours, level):
        with pytest.raises(ValueError):
            Cook("Иван", PHONE, "", 30, hours, level)


class TestKitchenWorker:
    def test_shift(self):
        worker = KitchenWorker("Пётр", PHONE, "", 40, "мойщик", 6)
        worker.extend_shift(2)
        worker.change_position(" кладовщик ")
        assert worker.position == "кладовщик" and worker.finish_shift() == 8 and worker.shift_hours == 0
        with pytest.raises(ValueError):
            worker.extend_shift(30)
        with pytest.raises(ValueError):
            worker.change_position("")


class TestKitchenAssistant:
    def test_work_area(self):
        assistant = KitchenAssistant("Оля", PHONE, "", 19, "холодный цех")
        clean_pan, dirty_pan = FryingPan("Сковорода", "чугун"), FryingPan("Сотейник", "сталь", is_clean=False)
        tools = [clean_pan, dirty_pan]
        assert assistant.count_unclean_tools(tools) == 1
        assert assistant.prepare_work_area(tools) == 1 and assistant.count_unclean_tools(tools) == 0
        assistant.change_area("горячий цех")
        assert assistant.assigned_area == "горячий цех"
        with pytest.raises(ValueError):
            assistant.change_area(" ")


class TestNutritionist:
    def test_review(self, dish):
        nutritionist = Nutritionist("Ольга", "", "olga@example.com", 40, "диетолог")
        assert nutritionist.qualification == "диетолог" and nutritionist.review_plan(DietPlan("План", meals=[dish]))
        assert not nutritionist.review_plan(DietPlan("Строгий", daily_calorie_limit=10, meals=[dish]))
        nutritionist.add_experience(2)
        assert nutritionist.experience_years == 2
        with pytest.raises(TypeError):
            nutritionist.review_plan("план")
        with pytest.raises(ValueError):
            nutritionist.add_experience(0)
        with pytest.raises(ValueError):
            Nutritionist("Ольга", "", "olga@example.com", 40, "диетолог", -1)
