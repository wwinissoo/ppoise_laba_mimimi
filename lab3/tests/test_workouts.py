from datetime import date, datetime, timedelta

import pytest

from fitness.exceptions import (
    EntityNotFoundError,
    InjuryRiskError,
    InvalidValueError,
    ScheduleConflictError,
    WorkoutStateError,
)
from fitness.users import Injury, Trainer
from fitness.workouts import (
    ExerciseSet,
    RestTimer,
    TemplateItem,
    TrainingSession,
    Workout,
    WorkoutEntry,
    WorkoutPlan,
    WorkoutTemplate,
)
from tests.conftest import NOW, TODAY


def done(reps, weight, rpe=8):
    exercise_set = ExerciseSet(reps, weight)
    exercise_set.complete(rpe)
    return exercise_set


class TestExerciseSet:
    def test_behaviour(self):
        exercise_set = ExerciseSet(10, 50)
        assert exercise_set.volume() == 500 and exercise_set.intensity_label() == "не выполнен"
        exercise_set.complete(6)
        assert exercise_set.completed and exercise_set.rpe == 6 and exercise_set.intensity_label() == "лёгкий"
        assert done(1, 1, 8).intensity_label() == "средний" and done(1, 1, 10).intensity_label() == "тяжёлый"
        assert ExerciseSet(0, duration_seconds=60).duration_seconds == 60 and exercise_set.reps == 10
        assert exercise_set.weight_kg == 50
        with pytest.raises(InvalidValueError):
            ExerciseSet(0)
        with pytest.raises(InvalidValueError):
            exercise_set.complete(11)


class TestWorkoutEntry:
    def test_sets(self, bench_press, running):
        entry = WorkoutEntry(bench_press, " тяжело ")
        assert entry.best_set() is None and entry.estimated_one_rep_max() == 0 and entry.note == "тяжело"
        entry.add_set(done(10, 60))
        entry.add_set(done(5, 80))
        entry.add_set(ExerciseSet(8, 70))
        assert entry.total_volume() == 1000 and entry.best_set().weight_kg == 80 and len(entry.completed_sets()) == 2
        assert entry.estimated_one_rep_max() == 93.3 and entry.exercise is bench_press and len(entry.sets) == 3
        with pytest.raises(InvalidValueError):
            entry.add_set(ExerciseSet(1, 500))
        assert entry.remove_set(2).weight_kg == 70
        with pytest.raises(EntityNotFoundError):
            entry.remove_set(5)
        cardio = WorkoutEntry(running, None)
        cardio.add_set(_timed())
        assert cardio.total_duration_seconds() == 600 and cardio.estimated_one_rep_max() == 0


def _timed():
    exercise_set = ExerciseSet(0, duration_seconds=600)
    exercise_set.complete(7)
    return exercise_set


class TestWorkout:
    def test_lifecycle(self, user, bench_press, chest):
        workout = Workout("Грудь", user, NOW)
        with pytest.raises(WorkoutStateError):
            workout.start(NOW)
        entry = workout.add_entry(WorkoutEntry(bench_press))
        assert workout.find_entry("жим лёжа") is entry and workout.find_entry("бег") is None
        assert workout.duration_minutes() == 0 and workout.estimate_calories(60) == 0
        workout.start(NOW)
        with pytest.raises(WorkoutStateError):
            workout.finish(NOW + timedelta(minutes=30))
        entry.add_set(done(10, 60))
        with pytest.raises(WorkoutStateError):
            workout.finish(NOW - timedelta(minutes=1))
        workout.finish(NOW + timedelta(minutes=60))
        assert workout.status == Workout.COMPLETED and workout.duration_minutes() == 60
        assert workout.total_volume() == 600 and workout.completed_sets_count() == 1
        assert workout.muscles_worked() == {chest} and workout.estimate_calories(60) == 378
        assert (workout.title, workout.user, workout.planned_start) == ("Грудь", user, NOW)
        assert workout.started_at == NOW and workout.finished_at == NOW + timedelta(hours=1) and workout.entries
        with pytest.raises(WorkoutStateError):
            workout.add_entry(WorkoutEntry(bench_press))
        with pytest.raises(WorkoutStateError):
            workout.cancel()

    def test_cancel_and_injury(self, user, bench_press, chest):
        workout = Workout("Отмена", user, NOW)
        workout.cancel()
        assert workout.status == Workout.CANCELLED
        user.health_profile.add_injury(Injury(chest, Injury.MILD, TODAY))
        with pytest.raises(InjuryRiskError):
            Workout("Травма", user, NOW).add_entry(WorkoutEntry(bench_press))


class TestPlanning:
    def test_template_item(self, bench_press):
        item = TemplateItem(bench_press, 3, 10, 60, 90)
        assert item.estimated_minutes() == 4.5 and item.planned_volume() == 1800
        entry = item.to_entry()
        assert len(entry.sets) == 3 and entry.note == "по шаблону" and item.exercise is bench_press
        assert (item.target_sets, item.target_reps, item.target_weight_kg, item.rest_seconds) == (3, 10, 60, 90)

    def test_template(self, user, bench_press, running, chest, legs):
        template = WorkoutTemplate("Фулбади", "новичок")
        with pytest.raises(InvalidValueError):
            template.instantiate(user, NOW)
        template.add_item(TemplateItem(bench_press, 3, 10, 60))
        template.add_item(TemplateItem(running, 1, 1))
        assert template.estimated_duration() == 4.6 and template.target_muscles() == {chest, legs}
        workout = template.instantiate(user, NOW)
        assert workout.title == "Фулбади" and len(workout.entries) == 2 and template.level == "новичок"
        assert template.remove_item("бег").exercise is running and len(template.items) == 1 and template.name
        with pytest.raises(EntityNotFoundError):
            template.remove_item("бег")
        with pytest.raises(InvalidValueError):
            WorkoutTemplate("X", "мастер")

    def test_plan(self, user, bench_press):
        template = WorkoutTemplate("Грудь", "средний")
        template.add_item(TemplateItem(bench_press, 2, 5, 80))
        plan = WorkoutPlan("Масса", date(2026, 11, 16), 4)
        plan.assign(0, template)
        plan.assign(3, template)
        assert plan.end_date() == date(2026, 12, 13) and plan.sessions_per_week() == 2 and plan.total_sessions() == 8
        assert plan.template_for(date(2026, 11, 16)) is template and plan.is_rest_day(date(2026, 11, 17))
        assert plan.template_for(date(2027, 1, 4)) is None and plan.schedule == {0: template, 3: template}
        workout = plan.schedule_workout(user, date(2026, 11, 19), 9)
        assert workout.planned_start == datetime(2026, 11, 19, 9)
        with pytest.raises(EntityNotFoundError):
            plan.schedule_workout(user, date(2026, 11, 17))
        plan.unassign(3)
        with pytest.raises(EntityNotFoundError):
            plan.unassign(3)
        with pytest.raises(InvalidValueError):
            plan.assign(7, template)
        assert plan.name == "Масса" and plan.start_date == date(2026, 11, 16) and plan.weeks == 4


class TestTrainingSession:
    def test_flow(self, user, other_user):
        trainer = Trainer("Олег", ["силовая"], 2000)
        session = TrainingSession(trainer, user, NOW, 60)
        other = TrainingSession(trainer, other_user, NOW + timedelta(minutes=30))
        far = TrainingSession(Trainer("Ира", ["йога"], 1000), other_user, NOW)
        assert session.overlaps(other) and not session.overlaps(far) and session.fee() == 2000
        with pytest.raises(ScheduleConflictError):
            session.reschedule(NOW + timedelta(minutes=15), [session, other])
        assert session.starts_at == NOW
        session.reschedule(NOW + timedelta(hours=2), [other])
        assert session.ends_at() == NOW + timedelta(hours=3) and session.status == TrainingSession.BOOKED
        assert session.cancel(NOW) == 1000 and session.status == TrainingSession.CANCELLED
        with pytest.raises(WorkoutStateError):
            session.complete()
        assert other.cancel(NOW - timedelta(days=2)) == 0
        far.complete()
        assert far.status == TrainingSession.DONE and far.trainer.full_name == "Ира" and far.client is other_user
        assert far.duration_minutes == 60


class TestRestTimer:
    def test_timer(self):
        timer = RestTimer(60)
        assert timer.tick(10) == 60
        timer.start()
        assert timer.running and timer.tick(20) == 40 and timer.elapsed_seconds == 20
        timer.pause()
        assert timer.tick(20) == 40
        timer.add_time(30)
        timer.start()
        assert timer.tick(100) == 0 and timer.is_finished() and not timer.running and timer.duration_seconds == 90
        with pytest.raises(InvalidValueError):
            timer.start()
        timer.reset()
        assert timer.remaining() == 90
