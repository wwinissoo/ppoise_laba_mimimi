from fitness.goals.constants import DAYS_PER_WEEK
from fitness.goals.fitness_goal import FitnessGoal
from fitness.users.body_measurement import BodyMeasurement
from fitness.validation import ensure_instance, ensure_positive


class WeightGoal(FitnessGoal):
    """Цель по весу тела (снижение или набор)."""

    def __init__(self, start_weight_kg, target_weight_kg, deadline):
        super().__init__("Вес тела", ensure_positive(start_weight_kg, "стартовый вес"), target_weight_kg, deadline)
        ensure_positive(target_weight_kg, "целевой вес")

    def is_weight_loss(self):
        return self.target_value < self.start_value

    def record_measurement(self, measurement):
        ensure_instance(measurement, BodyMeasurement, "замер")
        return self.update_progress(measurement.weight_kg)

    def weekly_change_needed(self, today):
        weeks = max(self.days_left(today), 1) / DAYS_PER_WEEK
        return round((self.target_value - self.current_value) / weeks, 2)
