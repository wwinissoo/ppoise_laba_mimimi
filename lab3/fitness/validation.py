"""Общие проверки входных данных для классов предметной области."""

from fitness.exceptions import InvalidValueError


def is_numeric(value):
    """True для int/float, но не для bool."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def ensure_text(value, field_name):
    """Непустая строка без крайних пробелов."""
    if not isinstance(value, str) or not value.strip():
        raise InvalidValueError(f"Поле «{field_name}» должно быть непустой строкой")
    return value.strip()


def ensure_number(value, field_name, minimum=None, maximum=None):
    """Число в границах [minimum, maximum] (границы необязательны)."""
    if not is_numeric(value):
        raise InvalidValueError(f"Поле «{field_name}» должно быть числом")
    if minimum is not None and value < minimum:
        raise InvalidValueError(f"Поле «{field_name}» не может быть меньше {minimum}")
    if maximum is not None and value > maximum:
        raise InvalidValueError(f"Поле «{field_name}» не может быть больше {maximum}")
    return value


def ensure_positive(value, field_name):
    """Строго положительное число."""
    ensure_number(value, field_name)
    if value <= 0:
        raise InvalidValueError(f"Поле «{field_name}» должно быть больше нуля")
    return value


def ensure_count(value, field_name, minimum=0):
    """Целое число (не bool) не меньше minimum."""
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise InvalidValueError(f"Поле «{field_name}» должно быть целым числом не меньше {minimum}")
    return value


def ensure_choice(value, allowed, field_name):
    """Значение из допустимого набора."""
    if value not in allowed:
        options = ", ".join(sorted(str(item) for item in allowed))
        raise InvalidValueError(f"Поле «{field_name}» должно быть одним из: {options}")
    return value


def ensure_instance(value, expected_type, field_name):
    """Объект нужного класса (ассоциация между классами модели)."""
    if not isinstance(value, expected_type):
        raise TypeError(f"Поле «{field_name}» должно быть объектом {expected_type.__name__}")
    return value
