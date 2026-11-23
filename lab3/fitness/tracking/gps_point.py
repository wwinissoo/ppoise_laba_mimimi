from datetime import datetime
import math

from fitness.exceptions import InvalidMeasurementError, InvalidValueError
from fitness.tracking.constants import EARTH_RADIUS_KM
from fitness.validation import ensure_instance, ensure_number


class GpsPoint:
    """Координата трека с высотой и временем фиксации."""

    def __init__(self, latitude, longitude, recorded_at, altitude_m=0):
        try:
            self._latitude = ensure_number(latitude, "широта", -90, 90)
            self._longitude = ensure_number(longitude, "долгота", -180, 180)
        except InvalidValueError as error:
            raise InvalidMeasurementError(str(error)) from None
        self._recorded_at = ensure_instance(recorded_at, datetime, "время фиксации")
        self._altitude_m = ensure_number(altitude_m, "высота")

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def recorded_at(self):
        return self._recorded_at

    @property
    def altitude_m(self):
        return self._altitude_m

    def distance_to(self, other):
        """Расстояние по формуле гаверсинусов, км."""
        ensure_instance(other, GpsPoint, "точка")
        lat1, lat2 = math.radians(self._latitude), math.radians(other.latitude)
        d_lat = lat2 - lat1
        d_lon = math.radians(other.longitude - self._longitude)
        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))

    def seconds_to(self, other):
        return (other.recorded_at - self._recorded_at).total_seconds()
