from datetime import timedelta

from fitness.validation import ensure_choice, ensure_positive, ensure_text


class MuscleGroup:
    """Группа мышц с нормой восстановления после нагрузки."""

    UPPER = "верх"
    LOWER = "низ"
    CORE = "кор"
    REGIONS = {UPPER, LOWER, CORE}

    def __init__(self, name, region, recovery_hours=48):
        self._name = ensure_text(name, "название группы мышц")
        self._region = ensure_choice(region, self.REGIONS, "область тела")
        self._recovery_hours = ensure_positive(recovery_hours, "часы восстановления")

    @property
    def name(self):
        return self._name

    @property
    def region(self):
        return self._region

    @property
    def recovery_hours(self):
        return self._recovery_hours

    def __eq__(self, other):
        return isinstance(other, MuscleGroup) and self._name.casefold() == other.name.casefold()

    def __hash__(self):
        return hash(self._name.casefold())

    def __repr__(self):
        return f"MuscleGroup({self._name!r})"

    def is_upper_body(self):
        return self._region == self.UPPER

    def hours_until_recovered(self, last_trained_at, now):
        ready_at = last_trained_at + timedelta(hours=self._recovery_hours)
        remaining = (ready_at - now).total_seconds() / 3600
        return max(0.0, round(remaining, 1))

    def is_recovered(self, last_trained_at, now):
        return self.hours_until_recovered(last_trained_at, now) == 0
