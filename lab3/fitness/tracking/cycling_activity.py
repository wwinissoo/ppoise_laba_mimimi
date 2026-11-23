from fitness.tracking.activity import Activity
from fitness.tracking.constants import MINUTES_PER_HOUR
from fitness.tracking.route import Route
from fitness.validation import ensure_choice, ensure_instance


class CyclingActivity(Activity):
    """Велозаезд по GPS-маршруту."""

    MET = 7.5
    KIND = "велосипед"
    BIKE_TYPES = {"шоссейный", "горный", "городской", "велотренажёр"}

    def __init__(self, user, started_at, duration_minutes, route, bike_type="городской"):
        super().__init__(user, started_at, duration_minutes)
        self._route = ensure_instance(route, Route, "маршрут")
        self._bike_type = ensure_choice(bike_type, self.BIKE_TYPES, "тип велосипеда")

    @property
    def route(self):
        return self._route

    @property
    def bike_type(self):
        return self._bike_type

    def distance_km(self):
        return self._route.total_distance_km()

    def average_speed_kmh(self):
        return round(self.distance_km() / self._duration_minutes * MINUTES_PER_HOUR, 1)

    def climbing_rate(self):
        """Набор высоты на километр, м/км."""
        distance = self.distance_km()
        return round(self._route.elevation_gain_m() / distance, 1) if distance else 0.0
