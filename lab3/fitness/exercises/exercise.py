from fitness.exercises.constants import MAX_LEVEL, MET_DIVISOR, MET_OXYGEN_FACTOR, MIN_LEVEL
from fitness.exercises.equipment import Equipment
from fitness.exercises.muscle_group import MuscleGroup
from fitness.validation import ensure_instance, ensure_number, ensure_positive, ensure_text


class Exercise:
    """Упражнение с основной группой мышц, сложностью и MET-коэффициентом."""

    CATEGORY = "общее"

    def __init__(self, name, primary_muscle, difficulty, met_value, equipment=(), secondary_muscles=()):
        self._name = ensure_text(name, "название упражнения")
        self._primary_muscle = ensure_instance(primary_muscle, MuscleGroup, "основная группа мышц")
        self._difficulty = ensure_number(difficulty, "сложность", MIN_LEVEL, MAX_LEVEL)
        self._met_value = ensure_positive(met_value, "MET")
        self._equipment = [ensure_instance(item, Equipment, "инвентарь") for item in equipment]
        self._secondary_muscles = [ensure_instance(item, MuscleGroup, "доп. группа мышц") for item in secondary_muscles]

    @property
    def name(self):
        return self._name

    @property
    def primary_muscle(self):
        return self._primary_muscle

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def met_value(self):
        return self._met_value

    @property
    def equipment(self):
        return tuple(self._equipment)

    @property
    def secondary_muscles(self):
        return tuple(self._secondary_muscles)

    def involved_muscles(self):
        return (self._primary_muscle, *self._secondary_muscles)

    def targets(self, muscle):
        return muscle in self.involved_muscles()

    def requires(self, equipment):
        return equipment in self._equipment

    def suits_level(self, level):
        return self._difficulty <= level

    def is_available(self):
        return all(item.in_service for item in self._equipment)

    def calories_burned(self, body_weight_kg, minutes):
        ensure_positive(body_weight_kg, "вес")
        ensure_number(minutes, "минуты", minimum=0)
        return round(self._met_value * MET_OXYGEN_FACTOR * body_weight_kg / MET_DIVISOR * minutes, 1)

    def describe(self):
        return f"{self._name} [{self.CATEGORY}], сложность {self._difficulty}/{MAX_LEVEL}"
