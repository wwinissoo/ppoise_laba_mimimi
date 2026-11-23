from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class GoalStateError(FitnessTrackerError):
    """Действие невозможно в текущем статусе цели."""
