from fitness.exceptions import NutritionLimitError
from fitness.validation import ensure_count, ensure_positive, ensure_text


class Supplement:
    """Добавка (креатин, витамин D…) с максимальной суточной дозой."""

    def __init__(self, name, dose_mg, max_daily_mg):
        self._name = ensure_text(name, "название добавки")
        self._dose_mg = ensure_positive(dose_mg, "разовая доза")
        self._max_daily_mg = ensure_positive(max_daily_mg, "суточный максимум")
        if self._dose_mg > self._max_daily_mg:
            raise NutritionLimitError("Разовая доза больше суточного максимума")
        self._taken_today_mg = 0

    @property
    def name(self):
        return self._name

    @property
    def dose_mg(self):
        return self._dose_mg

    @property
    def max_daily_mg(self):
        return self._max_daily_mg

    @property
    def taken_today_mg(self):
        return self._taken_today_mg

    def take(self, doses=1):
        ensure_count(doses, "количество доз", minimum=1)
        amount = self._dose_mg * doses
        if self._taken_today_mg + amount > self._max_daily_mg:
            raise NutritionLimitError(f"Превышена суточная норма «{self._name}»: {self._max_daily_mg} мг")
        self._taken_today_mg += amount
        return self._taken_today_mg

    def remaining_mg(self):
        return self._max_daily_mg - self._taken_today_mg

    def doses_left(self):
        return int(self.remaining_mg() // self._dose_mg)

    def reset_day(self):
        self._taken_today_mg = 0
