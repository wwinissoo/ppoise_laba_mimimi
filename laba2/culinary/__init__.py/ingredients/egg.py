from ingredient import Ingredient

class Egg(Ingredient):
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 egg_size="M", shell_intact=True, yolk_color="жёлтый"):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        self.__egg_size = egg_size
        self.__shell_intact = bool(shell_intact)
        self.__yolk_color = yolk_color
        self.__is_cracked = False

    @property
    def egg_size(self): return self.__egg_size
    @property
    def shell_intact(self): return self.__shell_intact
    @property
    def yolk_color(self): return self.__yolk_color
    @property
    def is_cracked(self): return self.__is_cracked

    def crack(self):
        if not self.__shell_intact:
            raise ValueError("Скорлупа уже повреждена")
        self.__shell_intact = False
        self.__is_cracked = True
        return self.weight

    def check_shell(self):
        return self.__shell_intact

    def change_yolk_color_label(self, color):
        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет желтка не может быть пустым")
        self.__yolk_color = color.strip()

    def is_suitable_for_boiling(self):
        return self.__shell_intact and self.is_available
