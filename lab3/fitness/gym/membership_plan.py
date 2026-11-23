from fitness.gym.constants import DAYS_PER_MONTH
from fitness.validation import ensure_count, ensure_number, ensure_positive, ensure_text


class MembershipPlan:
    """Тариф абонемента."""

    def __init__(self, name, monthly_price, duration_months, includes_group_classes=False, max_freezes=1):
        self._name = ensure_text(name, "название тарифа")
        self._monthly_price = ensure_positive(monthly_price, "цена в месяц")
        self._duration_months = ensure_count(duration_months, "срок, мес.", minimum=1)
        self._includes_group_classes = bool(includes_group_classes)
        self._max_freezes = ensure_count(max_freezes, "лимит заморозок")

    @property
    def name(self):
        return self._name

    @property
    def monthly_price(self):
        return self._monthly_price

    @property
    def duration_months(self):
        return self._duration_months

    @property
    def includes_group_classes(self):
        return self._includes_group_classes

    @property
    def max_freezes(self):
        return self._max_freezes

    def total_price(self, discount_percent=0):
        ensure_number(discount_percent, "скидка", 0, 100)
        return round(self._monthly_price * self._duration_months * (1 - discount_percent / 100), 2)

    def duration_days(self):
        return self._duration_months * DAYS_PER_MONTH

    def price_per_day(self):
        return round(self.total_price() / self.duration_days(), 2)
