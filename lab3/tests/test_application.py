from datetime import date, timedelta

import pytest

from cli.console import create_library
from fitness import FitnessTracker
from fitness.exceptions import DuplicateEntityError, EntityNotFoundError, InvalidCredentialsError
from fitness.goals import DistanceGoal, FitnessGoal, StrengthGoal, WeightGoal
from fitness.nutrition import Food, FoodPortion, Meal
from fitness.users import BodyMeasurement, User
from tests.conftest import NOW, PASSWORD, TODAY

DEADLINE = date(2027, 1, 31)


@pytest.fixture
def tracker():
    tracker = FitnessTracker(library=create_library())
    tracker.register_user("anna", "anna@mail.ru", PASSWORD, date(2000, 5, 20), User.FEMALE)
    return tracker


class TestFitnessTracker:
    def test_accounts(self, tracker):
        with pytest.raises(DuplicateEntityError):
            tracker.register_user("ANNA", "a@b.ru", PASSWORD, date(2000, 1, 1), User.FEMALE)
        with pytest.raises(InvalidCredentialsError):
            tracker.login("anna", "wrong")
        with pytest.raises(InvalidCredentialsError):
            tracker.login("nobody", PASSWORD)
        with pytest.raises(InvalidCredentialsError):
            tracker.workouts()
        with pytest.raises(InvalidCredentialsError):
            tracker.logout()
        user = tracker.login("Anna", PASSWORD)
        assert tracker.current_user is user and tracker.get_user("anna") is user and tracker.users == (user,)
        assert len(tracker.achievements().achievements) == 3 and tracker.goals() == ()
        assert tracker.library.get("Жим лёжа") and tracker.calculator.activity_level == "средняя"
        with pytest.raises(EntityNotFoundError):
            tracker.get_user("ivan")
        tracker.logout()
        assert tracker.current_user is None

    def test_training_flow(self, tracker):
        tracker.login("anna", PASSWORD)
        bench = tracker.library.get("Жим лёжа")
        strength = tracker.add_goal(StrengthGoal(bench, 80, 100, DEADLINE))
        abandoned = tracker.add_goal(StrengthGoal(bench, 80, 90, DEADLINE))
        abandoned.abandon()
        tracker.add_goal(DistanceGoal("Бег", 10, DEADLINE))
        workout = tracker.plan_workout("Грудь", NOW)
        tracker.log_set(workout, "жим лёжа", 10, 60, 7)
        tracker.log_set(workout, "Жим лёжа", 10, 75, 9)
        tracker.log_set(workout, "Приседания", 5, 80, 8)
        assert len(workout.entries) == 2 and strength.status == FitnessGoal.ACHIEVED
        assert abandoned.status == FitnessGoal.ABANDONED
        tracker.start_workout(workout, NOW)
        unlocked = tracker.finish_workout(workout, NOW + timedelta(minutes=45))
        assert [item.code for item in unlocked] == ["FIRST"] and tracker.streak().current_streak == 1
        assert tracker.notifications().unread_count() == 2 and tracker.workouts() == (workout,)
        report = tracker.progress_report(TODAY)
        assert report.workouts_count() == 1 and report.total_volume() == 1750

    def test_measurements_and_nutrition(self, tracker):
        user = tracker.login("anna", PASSWORD)
        weight = tracker.add_goal(WeightGoal(62, 60, DEADLINE))
        stale = tracker.add_goal(WeightGoal(62, 55, DEADLINE))
        stale.abandon()
        tracker.add_goal(DistanceGoal("Бег", 10, DEADLINE))
        tracker.record_measurement(BodyMeasurement(TODAY, 60, 170))
        assert weight.is_achieved() and stale.current_value == 62 and user.latest_measurement().weight_kg == 60
        meal = Meal("обед", NOW)
        meal.add_portion(FoodPortion(Food("Курица", 165, 31, 3.6, 0), 200))
        tracker.log_meal(meal)
        diary = tracker.diary_for(TODAY)
        assert diary.total_calories() == 330 and diary.calorie_target == 2127
        assert tracker.diary_for(TODAY, "похудение") is diary
