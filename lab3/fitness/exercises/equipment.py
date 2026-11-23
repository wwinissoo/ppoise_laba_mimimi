from fitness.exceptions import InvalidValueError
from fitness.validation import ensure_number, ensure_text


class Equipment:
    """Тренажёр или свободный вес с ограничением по нагрузке."""

    def __init__(self, name, category, max_load_kg, adjustable=False):
        self._name = ensure_text(name, "название инвентаря")
        self._category = ensure_text(category, "категория инвентаря")
        self._max_load_kg = ensure_number(max_load_kg, "максимальная нагрузка", minimum=0)
        self._adjustable = bool(adjustable)
        self._in_service = True

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @property
    def max_load_kg(self):
        return self._max_load_kg

    @property
    def adjustable(self):
        return self._adjustable

    @property
    def in_service(self):
        return self._in_service

    def can_handle(self, load_kg):
        return self._in_service and 0 <= load_kg <= self._max_load_kg

    def put_out_of_service(self):
        if not self._in_service:
            raise InvalidValueError(f"«{self._name}» уже на обслуживании")
        self._in_service = False

    def return_to_service(self):
        self._in_service = True
