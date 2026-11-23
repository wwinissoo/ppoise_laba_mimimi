from fitness.exceptions.invalid_value_error import InvalidValueError


class InvalidMeasurementError(InvalidValueError):
    """Физически невозможное измерение тела или показания датчика."""
