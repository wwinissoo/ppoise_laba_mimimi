from fitness.goals.fitness_goal import FitnessGoal
from fitness.tracking.activity import Activity
from fitness.validation import ensure_instance, ensure_positive


class DistanceGoal(FitnessGoal):
    """Накопительная цель по дистанции (км)."""

    def __init__(self, title, target_km, deadline):
        super().__init__(title, 0, ensure_positive(target_km, "целевая дистанция"), deadline)

    def record_activity(self, activity):
        ensure_instance(activity, Activity, "активность")
        return self.update_progress(round(self.current_value + activity.distance_km(), 3))

    def remaining_km(self):
        return round(max(0.0, self.target_value - self.current_value), 3)
