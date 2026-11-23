from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class InvalidValueError(FitnessTrackerError, ValueError):
    """Некорректное входное значение (пустая строка, отрицательное число и т. п.)."""
