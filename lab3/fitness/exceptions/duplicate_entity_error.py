from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class DuplicateEntityError(FitnessTrackerError):
    """Объект с таким идентификатором уже зарегистрирован."""
