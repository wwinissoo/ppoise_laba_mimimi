from datetime import timedelta

import pytest

from fitness.exceptions import DevicePairingError, InvalidMeasurementError, NutritionLimitError, WorkoutStateError
from fitness.exercises import BalanceExercise, FlexibilityExercise
from fitness.goals import StreakTracker
from fitness.nutrition import NutritionDiary, Supplement
from fitness.tracking import DailyActivity, GpsPoint, Route, SleepRecord, SwimmingActivity, WearableDevice
from fitness.users import HealthProfile, Injury
from fitness.workouts import ExerciseSet, RestTimer, Workout, WorkoutEntry
from tests.conftest import NOW, TODAY


def completed_workout(user, exercise):
    workout = Workout("Грудь", user, NOW)
    entry = workout.add_entry(WorkoutEntry(exercise))
    entry.add_set(ExerciseSet(10, 50)).complete(7)
    workout.start(NOW)
    workout.finish(NOW + timedelta(minutes=40))
    return workout


class TestStreakFromWorkout:
    def test_completed_workout_extends_streak(self, user, bench_press):
        streak = StreakTracker("тренировки")
        assert streak.register_workout(completed_workout(user, bench_press)) == 1
        assert streak.last_day == TODAY

    def test_planned_workout_is_rejected(self, user):
        with pytest.raises(WorkoutStateError):
            StreakTracker("тренировки").register_workout(Workout("План", user, NOW))


class TestDiarySupplements:
    def test_supplement_is_logged_once(self, user):
        diary = NutritionDiary(user, TODAY, 2000)
        creatine = Supplement("Креатин", 5000, 10000)
        assert diary.take_supplement(creatine) == 5000
        assert diary.take_supplement(creatine) == 0
        assert diary.supplements == (creatine,)
        with pytest.raises(NutritionLimitError):
            diary.take_supplement(creatine)


class TestDailySleep:
    def test_recovery_depends_on_attached_sleep(self):
        day = DailyActivity(TODAY)
        assert not day.is_well_recovered() and day.sleep is None
        bed = NOW - timedelta(hours=26)
        day.attach_sleep(SleepRecord(bed, bed + timedelta(hours=8), 120, 100, 1))
        assert day.is_well_recovered()
        day.attach_sleep(SleepRecord(bed, bed + timedelta(hours=8), 10, 10, 5))
        assert not day.is_well_recovered()

    def test_sleep_from_other_day_is_rejected(self):
        bed = NOW - timedelta(days=3)
        with pytest.raises(InvalidMeasurementError):
            DailyActivity(TODAY).attach_sleep(SleepRecord(bed, bed + timedelta(hours=8), 60, 60))


class TestExerciseLinks:
    def test_rest_timer_for_exercise(self, bench_press):
        assert RestTimer.for_exercise(bench_press).duration_seconds == bench_press.recommended_rest_seconds()

    def test_route_calories_for_cardio(self, running):
        route = Route("Парк")
        route.add_point(GpsPoint(53.9, 27.56, NOW))
        route.add_point(GpsPoint(53.91, 27.56, NOW + timedelta(minutes=30)))
        assert route.calories_for(running, 60) == running.calories_burned(60, 30)

    def test_injury_and_stretching(self, chest, legs):
        stretch = FlexibilityExercise("Растяжка груди", chest, 1, 30)
        mild, severe = Injury(chest, Injury.MILD, TODAY), Injury(chest, Injury.SEVERE, TODAY)
        assert mild.allows_stretching(stretch) and not severe.allows_stretching(stretch)
        assert Injury(legs, Injury.SEVERE, TODAY).allows_stretching(stretch)
        severe.mark_recovered(TODAY)
        assert severe.allows_stretching(stretch)

    def test_balance_needs_spotter(self, legs):
        healthy, pressured = HealthProfile(60), HealthProfile(60, 150, 95)
        advanced = BalanceExercise("Ласточка", legs, 2, 4)
        assert not healthy.needs_spotter(advanced) and pressured.needs_spotter(advanced)
        assert healthy.needs_spotter(BalanceExercise("Стойка", legs, 1, 1))
        healthy.add_injury(Injury(legs, Injury.MILD, TODAY))
        assert healthy.needs_spotter(advanced)


class TestDeviceSwim:
    def test_import_swim_for_paired_user(self, user, other_user):
        device = WearableDevice("Band", "SN-1")
        swim = SwimmingActivity(user, NOW, 20, 25, 40)
        with pytest.raises(DevicePairingError):
            device.import_swim(swim, NOW)
        device.pair(user)
        assert device.import_swim(swim, NOW) == 1000 and device.last_synced_at == NOW
        with pytest.raises(DevicePairingError):
            device.import_swim(SwimmingActivity(other_user, NOW, 20, 25, 40), NOW)
