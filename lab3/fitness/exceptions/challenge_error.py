from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class ChallengeError(FitnessTrackerError):
    """Нарушены правила челленджа (не участник, челлендж неактивен и т. п.)."""
