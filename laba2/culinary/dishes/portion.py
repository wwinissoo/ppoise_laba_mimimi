class Portion:
    """Объект предметной области: Portion."""

    def __init__(self, dish, weight, price, table_number):
        self.__dish = dish
        self.__weight = weight
        self.__price = price
        self.__table_number = table_number

    @property
    def dish(self):
        return self.__dish

    @property
    def weight(self):
        return self.__weight

    @property
    def price(self):
        return self.__price

    @property
    def table_number(self):
        return self.__table_number

    def calculate_price_per_gram(self):
        if self.weight <= 0: raise ValueError('Вес должен быть положительным')
        return self.price / self.weight

    def is_for_table(self, number):
        return self.table_number == number

    def increase_weight(self, grams):
        if grams <= 0: raise ValueError('Добавка должна быть положительной')
        self.__weight += grams

