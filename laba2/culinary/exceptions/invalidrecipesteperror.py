from .culinaryerror import CulinaryError

class InvalidRecipeStepError(CulinaryError):
    """Некорректный шаг рецепта."""

    def __init__(self, message="Некорректный шаг рецепта"):
        super().__init__(message)
