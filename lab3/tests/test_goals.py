from datetime import date, timedelta

import pytest

from fitness.exceptions import (
    CapacityExceededError,
    ChallengeError,
    DuplicateEntityError,
    GoalStateError,
    InvalidValueError,
)
from fitness.goals import (
    Achievement,
    AchievementBoard,
    Challenge,
    ChallengeEntry,
    DistanceGoal,
    FitnessGoal,
    StreakTracker,
    StrengthGoal,
    WeightGoal,
)
from fitness.tracking import RunActivity
from fitness.users import BodyMeasurement, User
from fitness.workouts import ExerciseSet
from tests.conftest import NOW, TODAY
from tests.test_tracking import make_route

DEADLINE = date(2026, 12, 31)


def completed(reps, weight):
    exercise_set = ExerciseSet(reps, weight)
    exercise_set.complete(9)
    return exercise_set


class TestGoals:
    def test_generic_goal(self):
        goal = FitnessGoal("Планка, сек", 60, 120, DEADLINE)
        assert goal.days_left(TODAY) == 45 and not goal.is_overdue(TODAY) and goal.is_overdue(date(2027, 1, 1))
        goal.update_progress(30)
        assert goal.progress_percent() == 0 and goal.current_value == 30
        assert (goal.title, goal.start_value, goal.target_value, goal.deadline) == ("Планка, сек", 60, 120, DEADLINE)
        goal.abandon()
        assert goal.status == FitnessGoal.ABANDONED and not goal.is_overdue(date(2027, 1, 1))
        with pytest.raises(GoalStateError):
            goal.abandon()
        with pytest.raises(InvalidValueError):
            FitnessGoal("X", 1, 1, DEADLINE)

    def test_weight_goal(self):
        goal = WeightGoal(70, 65, DEADLINE)
        assert goal.is_weight_loss() and goal.weekly_change_needed(TODAY) == -0.78
        assert goal.record_measurement(BodyMeasurement(TODAY, 67.5, 170)) == FitnessGoal.ACTIVE
        assert goal.progress_percent() == 50
        goal.record_measurement(BodyMeasurement(TODAY, 65, 170))
        assert goal.is_achieved()
        with pytest.raises(GoalStateError):
            goal.update_progress(64)
        assert not WeightGoal(60, 65, DEADLINE).is_weight_loss()

    def test_distance_goal(self, user):
        goal = DistanceGoal("4 км", 4, DEADLINE)
        run = RunActivity(user, NOW, 10, make_route())
        goal.record_activity(run)
        assert goal.remaining_km() == 1.998 and not goal.is_achieved()
        goal.record_activity(run)
        assert goal.is_achieved() and goal.remaining_km() == 0

    def test_strength_goal(self, bench_press, chest):
        from fitness.exercises import StrengthExercise

        goal = StrengthGoal(bench_press, 80, 100, DEADLINE)
        assert goal.title == "1ПМ: Жим лёжа" and goal.exercise is bench_press
        assert goal.record_set(bench_press, ExerciseSet(10, 75)) == FitnessGoal.ACTIVE
        assert goal.record_set(bench_press, completed(1, 50)) == FitnessGoal.ACTIVE
        with pytest.raises(InvalidValueError):
            goal.record_set(StrengthExercise("Другое", chest, 1), completed(1, 50))
        assert goal.record_set(bench_press, completed(10, 75)) == FitnessGoal.ACHIEVED


class TestStreak:
    def test_streak(self):
        streak = StreakTracker("Тренировки")
        assert streak.is_broken(TODAY) and streak.habit == "Тренировки"
        assert streak.register(TODAY) == 1 and streak.register(TODAY) == 1
        assert streak.register(TODAY + timedelta(days=1)) == 2 and streak.register(TODAY + timedelta(days=3)) == 1
        assert (
            streak.longest_streak == 2 and streak.current_streak == 1 and streak.last_day == TODAY + timedelta(days=3)
        )
        assert not streak.is_broken(TODAY + timedelta(days=4)) and streak.is_broken(TODAY + timedelta(days=5))
        with pytest.raises(InvalidValueError):
            streak.register(TODAY)
        streak.reset()
        assert streak.current_streak == 0 and streak.last_day is None


class TestAchievements:
    def test_achievement_and_board(self, user):
        first = Achievement("first", "Первая", "тренировки", 1, 10)
        streak = Achievement("week", "Неделя", "серия", 7, 30)
        board = AchievementBoard(user)
        assert board.completion_percent() == 0 and first.code == "FIRST" and board.user is user
        board.add(first)
        board.add(streak)
        with pytest.raises(DuplicateEntityError):
            board.add(Achievement("FIRST", "Копия", "тренировки", 1))
        assert board.evaluate("тренировки", 0, NOW) == [] and board.evaluate("серия", 3, NOW) == []
        assert board.evaluate("тренировки", 1, NOW) == [first] and board.evaluate("тренировки", 5, NOW) == []
        assert board.total_points() == 10 and board.completion_percent() == 50 and board.unlocked() == [first]
        assert first.unlocked_at == NOW and first.is_unlocked() and len(board.achievements) == 2
        assert (first.title, first.metric, first.threshold, first.points) == ("Первая", "тренировки", 1, 10)
        with pytest.raises(GoalStateError):
            first.unlock(NOW)


class TestChallenge:
    def test_challenge(self, user, other_user, policy):
        third = User.register("olga", "olga@mail.ru", "Secret123", date(1999, 1, 1), User.FEMALE, policy)
        challenge = Challenge("10 км", "км", 10, TODAY, TODAY + timedelta(days=7), max_participants=2)
        challenge.join(user, TODAY)
        challenge.join(other_user, TODAY)
        with pytest.raises(DuplicateEntityError):
            challenge.join(user, TODAY)
        with pytest.raises(CapacityExceededError):
            challenge.join(third, TODAY)
        with pytest.raises(ChallengeError):
            challenge.join(third, TODAY + timedelta(days=8))
        with pytest.raises(ChallengeError):
            challenge.record(user, 5, TODAY - timedelta(days=1))
        with pytest.raises(ChallengeError):
            challenge.record(third, 5, TODAY)
        assert challenge.record(user, 6, TODAY) == 6 and challenge.record(user, 5, TODAY) == 11
        challenge.record(other_user, 3, TODAY)
        assert [entry.user for entry in challenge.leaderboard()] == [user, other_user]
        assert challenge.finishers() == [user] and challenge.participants == (user, other_user)
        with pytest.raises(ChallengeError):
            challenge.winner(TODAY)
        assert challenge.winner(TODAY + timedelta(days=8)) is user
        challenge.leave(user)
        challenge.leave(other_user)
        assert challenge.winner(TODAY + timedelta(days=8)) is None and challenge.is_active(TODAY)
        assert (challenge.title, challenge.metric, challenge.target_value, challenge.max_participants) == (
            "10 км",
            "км",
            10,
            2,
        )
        assert challenge.starts_on == TODAY and challenge.ends_on == TODAY + timedelta(days=7)
        with pytest.raises(ChallengeError):
            Challenge("X", "км", 1, TODAY, TODAY - timedelta(days=1))

    def test_entry(self, user):
        entry = ChallengeEntry(user)
        entry.add(2.5)
        assert entry.total == 2.5 and entry.contributions == 1 and entry.user is user
