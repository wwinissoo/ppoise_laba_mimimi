from fitness.exceptions import InvalidValueError
from fitness.exercises.strength_exercise import StrengthExercise
from fitness.validation import ensure_instance, ensure_number, ensure_positive


class RestTimer:
    """Таймер отдыха между подходами."""

    def __init__(self, duration_seconds):
        self._duration_seconds = ensure_positive(duration_seconds, "длительность отдыха")
        self._elapsed_seconds = 0
        self._running = False

    @classmethod
    def for_exercise(cls, exercise):
        ensure_instance(exercise, StrengthExercise, "силовое упражнение")
        return cls(exercise.recommended_rest_seconds())

    @property
    def duration_seconds(self):
        return self._duration_seconds

    @property
    def elapsed_seconds(self):
        return self._elapsed_seconds

    @property
    def running(self):
        return self._running

    def start(self):
        if self.is_finished():
            raise InvalidValueError("Таймер уже истёк, сбросьте его")
        self._running = True

    def pause(self):
        self._running = False

    def tick(self, seconds):
        ensure_number(seconds, "секунды", minimum=0)
        if self._running:
            self._elapsed_seconds = min(self._duration_seconds, self._elapsed_seconds + seconds)
            self._running = not self.is_finished()
        return self.remaining()

    def remaining(self):
        return self._duration_seconds - self._elapsed_seconds

    def is_finished(self):
        return self._elapsed_seconds >= self._duration_seconds

    def add_time(self, seconds):
        self._duration_seconds += ensure_positive(seconds, "добавочное время")

    def reset(self):
        self._elapsed_seconds = 0
        self._running = False
