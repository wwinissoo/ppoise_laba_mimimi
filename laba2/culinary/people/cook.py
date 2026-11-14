"""Повар без закреплённой специализации."""

from culinary.units import HOURS_PER_DAY
from culinary.validation import require_number
from .person import Person


class Cook(Person):
    SKILL_LEVELS = ("начальный", "средний", "опытный", "мастер")
    MAX_SHIFT_HOURS = HOURS_PER_DAY
    DEFAULT_SHIFT_HOURS = 8

    def __init__(self, name, phone, email, age, shift_hours=DEFAULT_SHIFT_HOURS, skill_level="начальный"):
        super().__init__(name, phone, email, age)
        require_number(shift_hours, "Длительность смены должна быть положительной", positive=True)
        if shift_hours > self.MAX_SHIFT_HOURS:
            raise ValueError("Смена не может длиться больше суток")
        if skill_level not in self.SKILL_LEVELS:
            raise ValueError(f"Уровень должен быть одним из: {', '.join(self.SKILL_LEVELS)}")
        self.__shift_hours = shift_hours
        self.__skill_level = skill_level

    @property
    def shift_hours(self):
        return self.__shift_hours

    @property
    def skill_level(self):
        return self.__skill_level

    def estimate_shift_end(self, start_hour):
        if not isinstance(start_hour, int) or not 0 <= start_hour < HOURS_PER_DAY:
            raise ValueError("Час начала смены должен быть от 0 до 23")
        return (start_hour + self.shift_hours) % HOURS_PER_DAY

    def improve_skill(self):
        """Повышает уровень на одну ступень; возвращает новый уровень."""
        index = self.SKILL_LEVELS.index(self.__skill_level)
        if index == len(self.SKILL_LEVELS) - 1:
            raise ValueError("Достигнут максимальный уровень мастерства")
        self.__skill_level = self.SKILL_LEVELS[index + 1]
        return self.__skill_level
