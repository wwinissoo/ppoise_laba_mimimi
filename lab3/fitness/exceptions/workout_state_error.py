from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class WorkoutStateError(FitnessTrackerError):
    """Недопустимый переход статуса тренировки или действие в неверном статусе."""
