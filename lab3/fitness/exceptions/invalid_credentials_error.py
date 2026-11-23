from fitness.exceptions.authentication_error import AuthenticationError


class InvalidCredentialsError(AuthenticationError):
    """Неверная пара логин/пароль."""
