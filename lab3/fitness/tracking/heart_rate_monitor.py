from fitness.exceptions import InvalidMeasurementError
from fitness.tracking.heart_rate_sample import HeartRateSample
from fitness.tracking.heart_rate_zone import HeartRateZone
from fitness.validation import ensure_instance, ensure_number


class HeartRateMonitor:
    """Журнал пульса за активность с анализом по зонам."""

    DEFAULT_ZONES = (
        ("Разминка", 50, 60),
        ("Жиросжигание", 60, 70),
        ("Аэробная", 70, 80),
        ("Анаэробная", 80, 90),
        ("Максимальная", 90, 100),
    )

    def __init__(self, max_heart_rate, zones=None):
        self._max_heart_rate = ensure_number(max_heart_rate, "максимальный пульс", 100, 230)
        self._zones = list(zones) if zones else [HeartRateZone(*spec) for spec in self.DEFAULT_ZONES]
        for zone in self._zones:
            ensure_instance(zone, HeartRateZone, "зона")
        self._samples = []

    @property
    def max_heart_rate(self):
        return self._max_heart_rate

    @property
    def zones(self):
        return tuple(self._zones)

    @property
    def samples(self):
        return tuple(self._samples)

    def record(self, sample):
        ensure_instance(sample, HeartRateSample, "измерение")
        if self._samples and sample.recorded_at <= self._samples[-1].recorded_at:
            raise InvalidMeasurementError("Измерения пульса должны идти по времени")
        self._samples.append(sample)

    def average_bpm(self):
        return round(sum(item.bpm for item in self._samples) / len(self._samples)) if self._samples else 0

    def peak_bpm(self):
        return max((item.bpm for item in self._samples), default=0)

    def zone_of(self, bpm):
        for zone in self._zones:
            if zone.contains(bpm, self._max_heart_rate):
                return zone
        return None

    def seconds_in_zone(self, zone):
        """Время в зоне: каждый интервал приписывается зоне его начального измерения."""
        total = 0.0
        for current, following in zip(self._samples, self._samples[1:]):
            if zone.contains(current.bpm, self._max_heart_rate):
                total += (following.recorded_at - current.recorded_at).total_seconds()
        return total

    def exceeds_safe_limit(self):
        return self.peak_bpm() > self._max_heart_rate
