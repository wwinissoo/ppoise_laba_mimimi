"""Цели, серии, достижения и челленджи."""

from fitness.goals.achievement import Achievement
from fitness.goals.achievement_board import AchievementBoard
from fitness.goals.challenge import Challenge
from fitness.goals.challenge_entry import ChallengeEntry
from fitness.goals.distance_goal import DistanceGoal
from fitness.goals.fitness_goal import FitnessGoal
from fitness.goals.streak_tracker import StreakTracker
from fitness.goals.strength_goal import StrengthGoal
from fitness.goals.weight_goal import WeightGoal

__all__ = [
    "Achievement",
    "AchievementBoard",
    "Challenge",
    "ChallengeEntry",
    "DistanceGoal",
    "FitnessGoal",
    "StreakTracker",
    "StrengthGoal",
    "WeightGoal",
]
