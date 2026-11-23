from datetime import datetime

from fitness.exceptions import InvalidMeasurementError, InvalidValueError
from fitness.validation import ensure_instance, ensure_number


class HeartRateSample:
    """Одно измерение пульса."""

    MIN_BPM = 25
    MAX_BPM = 250

    def __init__(self, bpm, recorded_at):
        try:
            self._bpm = ensure_number(bpm, "пульс", self.MIN_BPM, self.MAX_BPM)
        except InvalidValueError as error:
            raise InvalidMeasurementError(str(error)) from None
        self._recorded_at = ensure_instance(recorded_at, datetime, "время измерения")

    @property
    def bpm(self):
        return self._bpm

    @property
    def recorded_at(self):
        return self._recorded_at

    def is_elevated(self, resting_bpm, margin=20):
        return self._bpm > resting_bpm + margin
