from datetime import datetime, time, timedelta

import pytest

from fitness.exceptions import InvalidValueError, ScheduleConflictError
from fitness.reports import Notification, NotificationCenter, ProgressReport, Reminder
from fitness.workouts import ExerciseSet, Workout, WorkoutEntry
from tests.conftest import NOW, TODAY


def finished_workout(user, exercise, start=NOW):
    workout = Workout("Тренировка", user, start)
    entry = workout.add_entry(WorkoutEntry(exercise))
    exercise_set = entry.add_set(ExerciseSet(10, 50))
    exercise_set.complete(8)
    workout.start(start)
    workout.finish(start + timedelta(minutes=40))
    return workout


class TestProgressReport:
    def test_report(self, user, other_user, bench_press):
        user.settings.set_weekly_target(4)
        workouts = [finished_workout(user, bench_press), Workout("План", user, NOW)]
        workouts.append(finished_workout(user, bench_press, NOW - timedelta(days=30)))
        report = ProgressReport(user, TODAY - timedelta(days=6), TODAY, workouts)
        assert report.workouts_count() == 1 and report.total_volume() == 500 and report.average_duration() == 40
        assert report.most_trained_muscle() == "Грудь" and report.consistency_percent() == 25
        assert report.summary() == "anna: 1 тренировок, объём 500 кг, в среднем 40 мин, регулярность 25.0%"
        assert report.user is user and report.period_end == TODAY and report.period_start and report.workouts
        empty = ProgressReport(user, TODAY, TODAY, [])
        assert empty.average_duration() == 0 and empty.most_trained_muscle() is None and empty.weeks_in_period() == 1
        with pytest.raises(InvalidValueError):
            ProgressReport(user, TODAY, TODAY, [finished_workout(other_user, bench_press)])
        with pytest.raises(InvalidValueError):
            ProgressReport(user, TODAY, TODAY - timedelta(days=1), [])


class TestReminders:
    def test_reminder(self):
        reminder = Reminder("Пей воду", time(9), {0, 2})
        monday = datetime(2026, 11, 16, 10)
        assert reminder.is_due(monday) and not reminder.is_due(datetime(2026, 11, 16, 8))
        reminder.mark_fired(monday)
        assert not reminder.is_due(monday) and reminder.next_occurrence(monday) == datetime(2026, 11, 18, 9)
        reminder.deactivate()
        assert not reminder.active and not reminder.is_due(datetime(2026, 11, 18, 10))
        reminder.activate()
        assert reminder.active and reminder.weekdays == (0, 2) and reminder.message and reminder.remind_at == time(9)
        assert reminder.clashes_with(Reminder("Другое", time(9), {2})) and not reminder.clashes_with(
            Reminder("Другое", time(10), {2})
        )
        assert Reminder("X", time(23, 59, 59, 999999), {0}).next_occurrence(
            datetime(2026, 11, 16, 23, 59, 59, 999999)
        ) == (datetime(2026, 11, 23, 23, 59, 59, 999999))
        for bad in (set(), {7}):
            with pytest.raises(ScheduleConflictError):
                Reminder("X", time(9), bad)

    def test_no_occurrence_branch(self, monkeypatch):
        reminder = Reminder("X", time(9), {0})
        monkeypatch.setattr(reminder, "_weekdays", frozenset())
        assert reminder.next_occurrence(NOW) is None


class TestNotificationCenter:
    def test_center(self, user):
        center = NotificationCenter(user)
        note = Notification("Привет", "Добро пожаловать", NOW)
        assert note.age_minutes(NOW + timedelta(minutes=5)) == 5 and center.push(note) and center.unread_count() == 1
        assert (note.title, note.body, note.created_at, note.read) == ("Привет", "Добро пожаловать", NOW, False)
        center.add_reminder(Reminder("Тренировка", time(18), {0}))
        with pytest.raises(ScheduleConflictError):
            center.add_reminder(Reminder("Ещё", time(18), {0, 1}))
        fired = center.process_reminders(NOW)
        assert len(fired) == 1 and center.process_reminders(NOW) == [] and center.unread_count() == 2
        center.mark_all_read()
        assert center.unread_count() == 0 and center.clear_read() == 2 and center.notifications == ()
        assert center.user is user and len(center.reminders) == 1
        user.settings.toggle_notifications()
        assert not center.push(note)
        assert center.process_reminders(NOW + timedelta(days=7)) == []
