from fitness.exceptions.fitness_tracker_error import FitnessTrackerError


class PaymentDeclinedError(FitnessTrackerError):
    """Платёж отклонён: неверная сумма, повторная оплата или возврат без оплаты."""
