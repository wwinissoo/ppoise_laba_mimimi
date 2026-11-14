import pytest

from culinary import units
from culinary.validation import (
    is_number,
    require_number,
    require_positive_int,
    require_text,
    require_transition,
)

TRANSITIONS = {"новый": {"готов"}, "готов": set()}


def test_is_number():
    assert is_number(1) and is_number(2.5) and not is_number(True) and not is_number("1")


def test_require_number():
    assert require_number(5, "ошибка", minimum=0) == 5
    for value, options in [("5", {}), (-1, {"minimum": 0}), (0, {"positive": True})]:
        with pytest.raises(ValueError, match="ошибка"):
            require_number(value, "ошибка", **options)
    with pytest.raises(KeyError):
        require_number(-1, "ошибка", KeyError, minimum=0)


def test_require_text():
    assert require_text("  текст ", "ошибка") == "текст"
    with pytest.raises(ValueError):
        require_text("  ", "ошибка")
    with pytest.raises(ValueError):
        require_text(None, "ошибка")


def test_require_positive_int():
    assert require_positive_int(3, "ошибка") == 3
    for value in (0, 1.5, True):
        with pytest.raises(ValueError):
            require_positive_int(value, "ошибка")


def test_require_transition():
    assert require_transition(TRANSITIONS, "новый", "готов", ValueError) == "готов"
    assert require_transition(TRANSITIONS, "готов", "готов", ValueError) == "готов"
    with pytest.raises(ValueError, match="Неизвестный"):
        require_transition(TRANSITIONS, "новый", "потерян", ValueError)
    with pytest.raises(ValueError, match="Нельзя"):
        require_transition(TRANSITIONS, "готов", "новый", ValueError)


def test_units():
    assert units.GRAMS_PER_KILOGRAM == 1000 and units.PERCENT == 100 and units.HOURS_PER_DAY == 24
