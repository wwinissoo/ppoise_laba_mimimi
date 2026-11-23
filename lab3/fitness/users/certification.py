from datetime import date

from fitness.validation import ensure_instance, ensure_text


class Certification:
    """Сертификат тренера со сроком действия."""

    def __init__(self, title, issuer, valid_until):
        self._title = ensure_text(title, "название сертификата")
        self._issuer = ensure_text(issuer, "организация")
        self._valid_until = ensure_instance(valid_until, date, "срок действия")

    @property
    def title(self):
        return self._title

    @property
    def issuer(self):
        return self._issuer

    @property
    def valid_until(self):
        return self._valid_until

    def is_valid(self, on_date):
        return on_date <= self._valid_until

    def days_until_expiry(self, on_date):
        return max(0, (self._valid_until - on_date).days)
