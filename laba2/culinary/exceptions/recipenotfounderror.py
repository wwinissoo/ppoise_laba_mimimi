from .culinaryerror import CulinaryError

class RecipeNotFoundError(CulinaryError):
    """Рецепт не найден."""

    def __init__(self, message="Рецепт не найден"):
        super().__init__(message)
