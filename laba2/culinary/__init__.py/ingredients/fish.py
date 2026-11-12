from ingredient import Ingredient

class Fish(Ingredient):
    def __init__(self, name, weight, price_per_kg, calories, expiration_days, storage_temperature,
                 fish_type="белая рыба", has_scales=True, bone_count=10):
        super().__init__(name, weight, price_per_kg, calories, expiration_days, storage_temperature)
        if bone_count < 0:
            raise ValueError("Количество костей не может быть отрицательным")
        self.__fish_type = fish_type
        self.__has_scales = bool(has_scales)
        self.__bone_count = bone_count
        self.__is_cleaned = False

    @property
    def fish_type(self): return self.__fish_type
    @property
    def has_scales(self): return self.__has_scales
    @property
    def bone_count(self): return self.__bone_count
    @property
    def is_cleaned(self): return self.__is_cleaned

    def remove_scales(self):
        self.__has_scales = False
        return True

    def remove_bones(self, removed_count=None):
        if removed_count is None:
            self.__bone_count = 0
        elif 0 <= removed_count <= self.__bone_count:
            self.__bone_count -= removed_count
        else:
            raise ValueError("Некорректное количество костей")
        return self.__bone_count

    def clean_fish(self):
        self.remove_scales()
        self.remove_bones()
        self.__is_cleaned = True
        return self.__is_cleaned

    def is_ready_for_cooking(self):
        return self.__is_cleaned and self.is_available
