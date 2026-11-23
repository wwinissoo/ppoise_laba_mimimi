from datetime import date, datetime

import pytest

from fitness.exercises import CardioExercise, Equipment, MuscleGroup, StrengthExercise
from fitness.users import BodyMeasurement, PasswordPolicy, User

PASSWORD = "Secret123"
TODAY = date(2026, 11, 16)
NOW = datetime(2026, 11, 16, 18, 0)


@pytest.fixture
def policy():
    return PasswordPolicy()


@pytest.fixture
def user(policy):
    return User.register("anna", "Anna@Example.com", PASSWORD, date(2000, 5, 20), User.FEMALE, policy)


@pytest.fixture
def other_user(policy):
    return User.register("ivan", "ivan@example.com", PASSWORD, date(1995, 1, 1), User.MALE, policy)


@pytest.fixture
def chest():
    return MuscleGroup("Грудь", MuscleGroup.UPPER)


@pytest.fixture
def legs():
    return MuscleGroup("Ноги", MuscleGroup.LOWER, 72)


@pytest.fixture
def barbell():
    return Equipment("Штанга", "свободные веса", 200)


@pytest.fixture
def bench_press(chest, barbell):
    return StrengthExercise("Жим лёжа", chest, 3, equipment=[barbell], compound=True)


@pytest.fixture
def running(legs):
    return CardioExercise("Бег", legs, 2, impact=CardioExercise.HIGH_IMPACT)


@pytest.fixture
def measurement():
    return BodyMeasurement(TODAY, 60, 170, 22, 70)
