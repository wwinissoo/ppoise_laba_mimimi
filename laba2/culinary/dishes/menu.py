class Menu:
    """Объект предметной области: Menu."""

    def __init__(self, title, dishes, valid_from, valid_to):
        self.__title = title
        self.__dishes = dishes
        self.__valid_from = valid_from
        self.__valid_to = valid_to

    @property
    def title(self):
        return self.__title

    @property
    def dishes(self):
        return self.__dishes

    @property
    def valid_from(self):
        return self.__valid_from

    @property
    def valid_to(self):
        return self.__valid_to

    def add_dish(self, dish):
        self.dishes.append(dish)

    def remove_dish(self, dish):
        if dish in self.dishes: self.dishes.remove(dish)

    def find_dishes_under_price(self, maximum):
        return [dish for dish in self.dishes if dish.recipe.estimate_total_cost() <= maximum]

