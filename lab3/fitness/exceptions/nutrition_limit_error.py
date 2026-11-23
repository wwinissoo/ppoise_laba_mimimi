from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class NutritionLimitError(FitnessTrackerError):
    """Превышена допустимая суточная норма добавки или питания."""
