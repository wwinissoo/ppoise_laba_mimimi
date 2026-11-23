"""Группы мышц, инвентарь и упражнения."""

from fitness.exercises.balance_exercise import BalanceExercise
from fitness.exercises.cardio_exercise import CardioExercise
from fitness.exercises.equipment import Equipment
from fitness.exercises.exercise import Exercise
from fitness.exercises.exercise_library import ExerciseLibrary
from fitness.exercises.flexibility_exercise import FlexibilityExercise
from fitness.exercises.muscle_group import MuscleGroup
from fitness.exercises.strength_exercise import StrengthExercise

__all__ = [
    "BalanceExercise",
    "CardioExercise",
    "Equipment",
    "Exercise",
    "ExerciseLibrary",
    "FlexibilityExercise",
    "MuscleGroup",
    "StrengthExercise",
]
