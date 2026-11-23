import pytest

from fitness import exceptions as ex
from fitness.validation import (
    ensure_choice,
    ensure_count,
    ensure_instance,
    ensure_number,
    ensure_positive,
    ensure_text,
    is_numeric,
)


class TestValidation:
    def test_is_numeric(self):
        assert is_numeric(1) and is_numeric(1.5) and not is_numeric(True) and not is_numeric("1")

    def test_text(self):
        assert ensure_text("  a ", "x") == "a"
        for bad in ("", "  ", None, 5):
            with pytest.raises(ex.InvalidValueError):
                ensure_text(bad, "x")

    def test_number_bounds(self):
        assert ensure_number(5, "x", 0, 10) == 5
        with pytest.raises(ex.InvalidValueError):
            ensure_number(-1, "x", minimum=0)
        with pytest.raises(ex.InvalidValueError):
            ensure_number(11, "x", maximum=10)
        with pytest.raises(ex.InvalidValueError):
            ensure_number("5", "x")

    def test_positive_count_choice_instance(self):
        assert ensure_positive(0.1, "x") == 0.1
        with pytest.raises(ex.InvalidValueError):
            ensure_positive(0, "x")
        assert ensure_count(3, "x", minimum=1) == 3
        for bad in (True, 1.0, -1):
            with pytest.raises(ex.InvalidValueError):
                ensure_count(bad, "x")
        assert ensure_choice("a", {"a", "b"}, "x") == "a"
        with pytest.raises(ex.InvalidValueError):
            ensure_choice("c", {"a", "b"}, "x")
        with pytest.raises(TypeError):
            ensure_instance("x", int, "x")


class TestExceptions:
    @pytest.mark.parametrize(
        "error, parent",
        [
            (ex.InvalidValueError, ValueError),
            (ex.InvalidMeasurementError, ex.InvalidValueError),
            (ex.WeakPasswordError, ex.AuthenticationError),
            (ex.InvalidCredentialsError, ex.AuthenticationError),
            (ex.EntityNotFoundError, LookupError),
            (ex.DuplicateEntityError, ex.FitnessTrackerError),
            (ex.WorkoutStateError, ex.FitnessTrackerError),
            (ex.InjuryRiskError, ex.FitnessTrackerError),
            (ex.GoalStateError, ex.FitnessTrackerError),
            (ex.DevicePairingError, ex.DeviceError),
            (ex.LowBatteryError, ex.DeviceError),
            (ex.MembershipExpiredError, ex.MembershipError),
            (ex.MembershipFrozenError, ex.MembershipError),
            (ex.PaymentDeclinedError, ex.FitnessTrackerError),
            (ex.CapacityExceededError, ex.FitnessTrackerError),
            (ex.ScheduleConflictError, ex.FitnessTrackerError),
            (ex.NutritionLimitError, ex.FitnessTrackerError),
            (ex.ChallengeError, ex.FitnessTrackerError),
        ],
    )
    def test_hierarchy(self, error, parent):
        assert issubclass(error, parent) and issubclass(error, ex.FitnessTrackerError)
        with pytest.raises(ex.FitnessTrackerError, match="сообщение"):
            raise error("сообщение")
