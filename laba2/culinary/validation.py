"""Общие проверки входных данных для классов предметной области."""


def is_number(value):
    """Число (int/float), но не bool."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_number(value, message, error=ValueError, minimum=None, positive=False):
    """Проверяет, что value — число, при необходимости положительное или не меньше minimum."""
    if not is_number(value) or (positive and value <= 0) or (minimum is not None and value < minimum):
        raise error(message)
    return value


def require_text(value, message, error=ValueError):
    """Проверяет, что value — непустая строка, и возвращает её без крайних пробелов."""
    if not isinstance(value, str) or not value.strip():
        raise error(message)
    return value.strip()


def require_positive_int(value, message, error=ValueError):
    """Проверяет, что value — положительное целое число (bool не допускается)."""
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise error(message)
    return value


def require_transition(transitions, current, target, error):
    """Проверяет переход конечного автомата статусов и возвращает новый статус."""
    if target not in transitions:
        raise error(f"Неизвестный статус «{target}»")
    if target != current and target not in transitions[current]:
        raise error(f"Нельзя изменить статус с «{current}» на «{target}»")
    return target
