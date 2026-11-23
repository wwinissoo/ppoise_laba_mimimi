from fitness.exceptions import InvalidMeasurementError
from fitness.exercises.cardio_exercise import CardioExercise
from fitness.tracking.constants import SECONDS_PER_MINUTE
from fitness.tracking.gps_point import GpsPoint
from fitness.validation import ensure_instance, ensure_positive, ensure_text


class Route:
    """Упорядоченный по времени трек."""

    def __init__(self, name):
        self._name = ensure_text(name, "название маршрута")
        self._points = []

    @property
    def name(self):
        return self._name

    @property
    def points(self):
        return tuple(self._points)

    def add_point(self, point):
        ensure_instance(point, GpsPoint, "точка")
        if self._points and point.recorded_at <= self._points[-1].recorded_at:
            raise InvalidMeasurementError("Точки маршрута должны идти в хронологическом порядке")
        self._points.append(point)

    def _segments(self):
        return zip(self._points, self._points[1:])

    def total_distance_km(self):
        return round(sum(start.distance_to(end) for start, end in self._segments()), 3)

    def elevation_gain_m(self):
        return sum(max(0, end.altitude_m - start.altitude_m) for start, end in self._segments())

    def duration_seconds(self):
        return self._points[0].seconds_to(self._points[-1]) if len(self._points) > 1 else 0

    def is_loop(self, tolerance_km=0.1):
        ensure_positive(tolerance_km, "допуск")
        return len(self._points) > 2 and self._points[0].distance_to(self._points[-1]) <= tolerance_km

    def calories_for(self, exercise, body_weight_kg):
        ensure_instance(exercise, CardioExercise, "кардиоупражнение")
        minutes = self.duration_seconds() / SECONDS_PER_MINUTE
        return exercise.calories_burned(body_weight_kg, minutes)
