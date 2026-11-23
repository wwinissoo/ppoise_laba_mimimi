from fitness.exceptions import InvalidValueError
from fitness.validation import ensure_choice, ensure_count, ensure_text


class UserSettings:
    """Единицы измерения, недельная цель и уведомления."""

    METRIC = "метрическая"
    IMPERIAL = "имперская"
    POUNDS_PER_KG = 2.20462
    MAX_WEEKLY_WORKOUTS = 14

    def __init__(self, unit_system=METRIC, weekly_workout_target=3, notifications_enabled=True, language="ru"):
        self._unit_system = ensure_choice(unit_system, {self.METRIC, self.IMPERIAL}, "система единиц")
        self._weekly_workout_target = ensure_count(weekly_workout_target, "тренировок в неделю", minimum=1)
        self._notifications_enabled = bool(notifications_enabled)
        self._language = ensure_text(language, "язык")

    @property
    def unit_system(self):
        return self._unit_system

    @property
    def weekly_workout_target(self):
        return self._weekly_workout_target

    @property
    def notifications_enabled(self):
        return self._notifications_enabled

    @property
    def language(self):
        return self._language

    def toggle_notifications(self):
        self._notifications_enabled = not self._notifications_enabled
        return self._notifications_enabled

    def switch_unit_system(self):
        self._unit_system = self.IMPERIAL if self._unit_system == self.METRIC else self.METRIC
        return self._unit_system

    def set_weekly_target(self, workouts):
        ensure_count(workouts, "тренировок в неделю", minimum=1)
        if workouts > self.MAX_WEEKLY_WORKOUTS:
            raise InvalidValueError(f"Не больше {self.MAX_WEEKLY_WORKOUTS} тренировок в неделю")
        self._weekly_workout_target = workouts

    def format_weight(self, weight_kg):
        if self._unit_system == self.IMPERIAL:
            return f"{weight_kg * self.POUNDS_PER_KG:.1f} lb"
        return f"{weight_kg:.1f} кг"
