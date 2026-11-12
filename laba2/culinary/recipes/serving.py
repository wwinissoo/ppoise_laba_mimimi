"""Описание подачи готового блюда."""
class Serving:
    """Хранит параметры подачи блюда."""
    def __init__(self, temperature_celsius, presentation, serving_size_grams):
        if temperature_celsius < -20 or temperature_celsius > 150:
            raise ValueError("Недопустимая температура подачи")
        if serving_size_grams <= 0:
            raise ValueError("Размер порции должен быть положительным")
        self.__temperature_celsius = temperature_celsius
        self.__presentation = str(presentation).strip()
        self.__serving_size_grams = serving_size_grams
    @property
    def temperature_celsius(self): return self.__temperature_celsius
    @property
    def presentation(self): return self.__presentation
    @property
    def serving_size_grams(self): return self.__serving_size_grams
    def describe(self):
        return f"Подача: {self.presentation}; {self.serving_size_grams} г; {self.temperature_celsius} °C"
