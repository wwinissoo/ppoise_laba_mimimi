class ChefSpecialization:
    """Объект предметной области: ChefSpecialization."""

    def __init__(self, title, allowed_categories, certification_level, years_required):
        self.__title = title
        self.__allowed_categories = allowed_categories
        self.__certification_level = certification_level
        self.__years_required = years_required

    @property
    def title(self):
        return self.__title

    @property
    def allowed_categories(self):
        return self.__allowed_categories

    @property
    def certification_level(self):
        return self.__certification_level

    @property
    def years_required(self):
        return self.__years_required

    def allows(self, category):
        return category in self.allowed_categories

    def is_certified(self):
        return self.certification_level > 0

    def experience_requirement_met(self, years):
        return years >= self.years_required

