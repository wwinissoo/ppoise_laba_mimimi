from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class EntityNotFoundError(FitnessTrackerError, LookupError):
    """Запрошенный объект (пользователь, упражнение, тренировка) не найден."""
