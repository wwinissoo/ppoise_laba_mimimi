from fitness.exceptions.authentication_error import AuthenticationError


class WeakPasswordError(AuthenticationError):
    """Пароль не удовлетворяет политике сложности."""
