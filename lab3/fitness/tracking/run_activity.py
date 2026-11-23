from fitness.exceptions import InvalidValueError
from fitness.tracking.activity import Activity
from fitness.tracking.route import Route
from fitness.validation import ensure_instance, ensure_positive


class RunActivity(Activity):
    """Пробежка по GPS-маршруту."""

    MET = 9.8
    KIND = "бег"
    RIEGEL_EXPONENT = 1.06

    def __init__(self, user, started_at, duration_minutes, route):
        super().__init__(user, started_at, duration_minutes)
        self._route = ensure_instance(route, Route, "маршрут")

    @property
    def route(self):
        return self._route

    def distance_km(self):
        return self._route.total_distance_km()

    def average_pace(self):
        """Темп, мин/км."""
        distance = self.distance_km()
        if distance == 0:
            raise InvalidValueError("Нельзя вычислить темп для нулевой дистанции")
        return round(self._duration_minutes / distance, 2)

    def predict_race_minutes(self, race_km):
        """Прогноз времени по формуле Ригеля."""
        ensure_positive(race_km, "дистанция забега")
        distance = self.distance_km()
        if distance == 0:
            raise InvalidValueError("Для прогноза нужна ненулевая дистанция")
        return round(self._duration_minutes * (race_km / distance) ** self.RIEGEL_EXPONENT, 1)
