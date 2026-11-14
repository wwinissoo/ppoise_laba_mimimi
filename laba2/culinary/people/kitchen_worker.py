from culinary.units import HOURS_PER_DAY
from culinary.validation import require_number, require_text
from .person import Person


class KitchenWorker(Person):
    """Работник кухни; использует общие поля Person."""

    MAX_SHIFT_HOURS = HOURS_PER_DAY

    def __init__(self, name, phone, email, age, position, shift_hours):
        super().__init__(name, phone, email, age)
        self.__position = require_text(position, "Должность не может быть пустой")
        self.__shift_hours = 0
        self.extend_shift(shift_hours)

    @property
    def position(self):
        return self.__position

    @property
    def shift_hours(self):
        return self.__shift_hours

    def change_position(self, position):
        self.__position = require_text(position, "Должность не может быть пустой")

    def extend_shift(self, hours):
        require_number(hours, "Добавочное время не может быть отрицательным", minimum=0)
        if self.__shift_hours + hours > self.MAX_SHIFT_HOURS:
            raise ValueError("Смена не может длиться больше суток")
        self.__shift_hours += hours

    def finish_shift(self):
        completed = self.__shift_hours
        self.__shift_hours = 0
        return completed
