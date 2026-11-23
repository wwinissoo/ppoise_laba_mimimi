from datetime import datetime

import pytest

from fitness.exceptions import DuplicateEntityError, EntityNotFoundError, InvalidValueError
from fitness.exercises import (
    BalanceExercise,
    CardioExercise,
    Exercise,
    ExerciseLibrary,
    FlexibilityExercise,
    MuscleGroup,
    StrengthExercise,
)
from fitness.users import HealthProfile, Injury
from tests.conftest import TODAY


class TestMuscleGroup:
    def test_recovery(self, chest, legs):
        trained = datetime(2026, 11, 15, 10)
        assert chest.hours_until_recovered(trained, datetime(2026, 11, 16, 10)) == 24
        assert chest.is_recovered(trained, datetime(2026, 11, 17, 11)) and chest.is_upper_body()
        assert not legs.is_upper_body() and legs.recovery_hours == 72 and legs.region == MuscleGroup.LOWER
        assert chest == MuscleGroup("грудь", MuscleGroup.UPPER) and chest != "Грудь"
        assert hash(chest) == hash(MuscleGroup("ГРУДЬ", MuscleGroup.CORE)) and "Грудь" in repr(chest)
        with pytest.raises(InvalidValueError):
            MuscleGroup("Шея", "голова")


class TestEquipment:
    def test_service(self, barbell):
        assert barbell.can_handle(100) and not barbell.can_handle(250) and not barbell.can_handle(-1)
        barbell.put_out_of_service()
        assert not barbell.in_service and not barbell.can_handle(10)
        with pytest.raises(InvalidValueError):
            barbell.put_out_of_service()
        barbell.return_to_service()
        assert barbell.in_service and barbell.category == "свободные веса" and barbell.max_load_kg == 200
        assert not barbell.adjustable and barbell.name == "Штанга"


class TestExercise:
    def test_base(self, chest, legs, barbell):
        exercise = Exercise("Отжимания", chest, 2, 4, secondary_muscles=[legs])
        assert exercise.involved_muscles() == (chest, legs) and exercise.targets(legs)
        assert not exercise.requires(barbell) and exercise.suits_level(2) and not exercise.suits_level(1)
        assert exercise.calories_burned(70, 30) == 147 and exercise.is_available()
        assert exercise.describe() == "Отжимания [общее], сложность 2/5"
        assert exercise.met_value == 4 and exercise.difficulty == 2 and exercise.primary_muscle is chest
        assert exercise.equipment == () and exercise.secondary_muscles == (legs,)
        with pytest.raises(InvalidValueError):
            Exercise("X", chest, 6, 3)
        with pytest.raises(TypeError):
            Exercise("X", chest, 1, 3, equipment=["гантель"])

    def test_strength(self, bench_press, barbell, chest):
        assert bench_press.estimate_one_rep_max(100, 1) == 100 and bench_press.estimate_one_rep_max(100, 10) == 133.3
        assert bench_press.recommended_rest_seconds() == 180 and bench_press.compound and bench_press.requires(barbell)
        assert StrengthExercise("Разводка", chest, 2).recommended_rest_seconds() == 90
        assert bench_press.check_load(150)
        with pytest.raises(InvalidValueError):
            bench_press.check_load(300)
        barbell.put_out_of_service()
        assert not bench_press.is_available()

    def test_cardio(self, running, legs):
        assert not running.is_low_impact() and running.impact == CardioExercise.HIGH_IMPACT
        assert running.pace_min_per_km(5, 25) == 5 and running.speed_kmh(5, 30) == 10
        assert CardioExercise("Велотренажёр", legs, 1).is_low_impact()
        with pytest.raises(InvalidValueError):
            CardioExercise("X", legs, 1, impact="средняя")
        with pytest.raises(InvalidValueError):
            running.pace_min_per_km(0, 10)

    def test_flexibility_and_balance(self, legs):
        stretch = FlexibilityExercise("Бабочка", legs, 1, 30)
        assert stretch.total_hold_time(3) == 180 and stretch.bilateral
        stretch.extend_hold(10)
        assert stretch.hold_seconds == 40
        assert FlexibilityExercise("Кобра", legs, 1, 20, bilateral=False).total_hold_time(2) == 40
        balance = BalanceExercise("Ласточка", legs, 2)
        assert balance.requires_support() and balance.progress() == 2 and balance.progress() == 3
        assert not balance.requires_support() and balance.stability_level == 3
        top = BalanceExercise("Bosu", legs, 4, stability_level=5)
        with pytest.raises(InvalidValueError):
            top.progress()


class TestExerciseLibrary:
    def test_crud_and_search(self, bench_press, running, barbell, chest, legs):
        library = ExerciseLibrary()
        library.add(bench_press)
        library.add(running)
        with pytest.raises(DuplicateEntityError):
            library.add(StrengthExercise("жим лёжа", chest, 1))
        assert library.get(" ЖИМ ЛЁЖА ") is bench_press and library.search("бег") == [running]
        assert library.find_by_muscle(legs) == [running] and library.find_by_equipment(barbell) == [bench_press]
        assert library.find_for_level(2) == [running] and len(library.exercises) == 2 and library.title
        profile = HealthProfile(60)
        profile.add_injury(Injury(chest, Injury.MILD, TODAY))
        assert library.safe_for(profile) == [running]
        assert library.remove("Бег") is running
        with pytest.raises(EntityNotFoundError):
            library.get("Бег")
