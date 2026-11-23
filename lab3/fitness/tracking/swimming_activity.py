from fitness.tracking.activity import Activity
from fitness.tracking.constants import METERS_PER_KM
from fitness.validation import ensure_choice, ensure_count, ensure_positive


class SwimmingActivity(Activity):
    """Плавание в бассейне."""

    MET = 8.0
    KIND = "плавание"
    STROKES = {"кроль", "брасс", "баттерфляй", "на спине"}
    PACE_DISTANCE_M = 100

    def __init__(self, user, started_at, duration_minutes, pool_length_m, laps, stroke="кроль"):
        super().__init__(user, started_at, duration_minutes)
        self._pool_length_m = ensure_positive(pool_length_m, "длина бассейна")
        self._laps = ensure_count(laps, "бассейны", minimum=1)
        self._stroke = ensure_choice(stroke, self.STROKES, "стиль")

    @property
    def pool_length_m(self):
        return self._pool_length_m

    @property
    def laps(self):
        return self._laps

    @property
    def stroke(self):
        return self._stroke

    def distance_meters(self):
        return self._pool_length_m * self._laps

    def distance_km(self):
        return self.distance_meters() / METERS_PER_KM

    def pace_per_100m(self):
        return round(self._duration_minutes / self.distance_meters() * self.PACE_DISTANCE_M, 2)

    def swolf(self, strokes_per_lap):
        """SWOLF = секунды на бассейн + гребки на бассейн (меньше — лучше)."""
        ensure_count(strokes_per_lap, "гребки", minimum=1)
        seconds_per_lap = self._duration_minutes * 60 / self._laps
        return round(seconds_per_lap + strokes_per_lap)
