from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class ScheduleConflictError(FitnessTrackerError):
    """Пересечение по времени занятий, сессий или напоминаний."""
