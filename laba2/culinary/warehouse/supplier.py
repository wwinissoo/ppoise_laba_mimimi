from culinary.exceptions import SupplierError
class Supplier:
    """Объект предметной области: Supplier."""

    def __init__(self, name, phone, products, rating):
        self.__name = name
        self.__phone = phone
        self.__products = products
        self.__rating = rating

    @property
    def name(self):
        return self.__name

    @property
    def phone(self):
        return self.__phone

    @property
    def products(self):
        return self.__products

    @property
    def rating(self):
        return self.__rating

    def add_product(self, ingredient):
        self.products.append(ingredient)

    def rate(self, score):
        if not 1 <= score <= 5: raise SupplierError('Оценка поставщика должна быть от 1 до 5')
        self.__rating = score

    def supplies(self, ingredient):
        return any(item.name == ingredient.name for item in self.products)

