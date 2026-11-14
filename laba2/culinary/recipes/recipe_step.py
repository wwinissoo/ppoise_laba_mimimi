from culinary.exceptions import InvalidRecipeStepError, InvalidTemperatureException
from culinary.validation import is_number, require_positive_int


class RecipeStep:
    """Один пронумерованный шаг приготовления блюда."""

    MIN_TEMPERATURE = -30
    MAX_TEMPERATURE = 300

    def __init__(self, number, instruction, duration_minutes, temperature):
        require_positive_int(number, "Номер шага должен быть положительным целым числом", InvalidRecipeStepError)
        if not isinstance(instruction, str) or not instruction.strip():
            raise InvalidRecipeStepError("Описание шага не может быть пустым")
        if not is_number(duration_minutes) or duration_minutes < 0:
            raise InvalidRecipeStepError("Длительность шага не может быть отрицательной")
        if temperature is not None and (
            not is_number(temperature) or not self.MIN_TEMPERATURE <= temperature <= self.MAX_TEMPERATURE
        ):
            raise InvalidTemperatureException(
                f"Температура шага должна быть от {self.MIN_TEMPERATURE} до {self.MAX_TEMPERATURE} °C"
            )
        self.__number = number
        self.__instruction = instruction.strip()
        self.__duration_minutes = duration_minutes
        self.__temperature = temperature

    @property
    def number(self):
        return self.__number

    @property
    def instruction(self):
        return self.__instruction

    @property
    def duration_minutes(self):
        return self.__duration_minutes

    @property
    def temperature(self):
        return self.__temperature

    def format_instruction(self):
        return f"{self.number}. {self.instruction}"

    def calculate_end_minute(self, start_minute):
        if start_minute < 0:
            raise InvalidRecipeStepError("Минута начала не может быть отрицательной")
        return start_minute + self.duration_minutes
