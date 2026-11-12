from culinary.exceptions import InvalidRecipeStepError

class RecipeStep:
    """Один пронумерованный шаг приготовления блюда."""

    def __init__(self, number, instruction, duration_minutes, temperature):
        if not isinstance(number, int) or number <= 0:
            raise InvalidRecipeStepError("Номер шага должен быть положительным целым числом")
        if not isinstance(instruction, str) or not instruction.strip():
            raise InvalidRecipeStepError("Описание шага не может быть пустым")
        if duration_minutes < 0:
            raise InvalidRecipeStepError("Длительность шага не может быть отрицательной")
        self.__number = number
        self.__instruction = instruction.strip()
        self.__duration_minutes = duration_minutes
        self.__temperature = temperature

    @property
    def number(self): return self.__number
    @property
    def instruction(self): return self.__instruction
    @property
    def duration_minutes(self): return self.__duration_minutes
    @property
    def temperature(self): return self.__temperature

    def format_instruction(self):
        return f"{self.number}. {self.instruction}"

    def calculate_end_minute(self, start_minute):
        if start_minute < 0:
            raise InvalidRecipeStepError("Минута начала не может быть отрицательной")
        return start_minute + self.duration_minutes
