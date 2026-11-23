"""Исключения фитнес-трекера."""

from fitness.exceptions.authentication_error import AuthenticationError
from fitness.exceptions.capacity_exceeded_error import CapacityExceededError
from fitness.exceptions.challenge_error import ChallengeError
from fitness.exceptions.device_error import DeviceError
from fitness.exceptions.device_pairing_error import DevicePairingError
from fitness.exceptions.duplicate_entity_error import DuplicateEntityError
from fitness.exceptions.entity_not_found_error import EntityNotFoundError
from fitness.exceptions.fitness_tracker_error import FitnessTrackerError
from fitness.exceptions.goal_state_error import GoalStateError
from fitness.exceptions.injury_risk_error import InjuryRiskError
from fitness.exceptions.invalid_credentials_error import InvalidCredentialsError
from fitness.exceptions.invalid_measurement_error import InvalidMeasurementError
from fitness.exceptions.invalid_value_error import InvalidValueError
from fitness.exceptions.low_battery_error import LowBatteryError
from fitness.exceptions.membership_error import MembershipError
from fitness.exceptions.membership_expired_error import MembershipExpiredError
from fitness.exceptions.membership_frozen_error import MembershipFrozenError
from fitness.exceptions.nutrition_limit_error import NutritionLimitError
from fitness.exceptions.payment_declined_error import PaymentDeclinedError
from fitness.exceptions.schedule_conflict_error import ScheduleConflictError
from fitness.exceptions.weak_password_error import WeakPasswordError
from fitness.exceptions.workout_state_error import WorkoutStateError

__all__ = [
    "AuthenticationError",
    "CapacityExceededError",
    "ChallengeError",
    "DeviceError",
    "DevicePairingError",
    "DuplicateEntityError",
    "EntityNotFoundError",
    "FitnessTrackerError",
    "GoalStateError",
    "InjuryRiskError",
    "InvalidCredentialsError",
    "InvalidMeasurementError",
    "InvalidValueError",
    "LowBatteryError",
    "MembershipError",
    "MembershipExpiredError",
    "MembershipFrozenError",
    "NutritionLimitError",
    "PaymentDeclinedError",
    "ScheduleConflictError",
    "WeakPasswordError",
    "WorkoutStateError",
]
