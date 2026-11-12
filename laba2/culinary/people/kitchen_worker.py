from .person import Person

class KitchenWorker(Person):
    """Работник кухни; использует общие поля Person."""

    def __init__(self, name, phone, email, age, position, shift_hours):
        super().__init__(name, phone, email, age)
        if shift_hours < 0: raise ValueError("Продолжительность смены не может быть отрицательной")
        self.__position = position
        self.__shift_hours = shift_hours

    @property
    def position(self): return self.__position
    @property
    def shift_hours(self): return self.__shift_hours

    def change_position(self, position):
        if not isinstance(position, str) or not position.strip():
            raise ValueError("Должность не может быть пустой")
        self.__position = position.strip()

    def extend_shift(self, hours):
        if hours < 0: raise ValueError("Добавочное время не может быть отрицательным")
        self.__shift_hours += hours

    def finish_shift(self):
        completed = self.__shift_hours
        self.__shift_hours = 0
        return completed
