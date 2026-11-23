from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class CapacityExceededError(FitnessTrackerError):
    """Превышена вместимость зала, группового занятия или шкафчиков."""
