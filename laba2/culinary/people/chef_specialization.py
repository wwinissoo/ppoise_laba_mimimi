from culinary.validation import require_text


class ChefSpecialization:
    """Специализация повара: допустимые категории блюд и требования к квалификации."""

    MAX_CERTIFICATION_LEVEL = 5

    def __init__(self, title, allowed_categories, certification_level=0, years_required=0):
        self.__title = require_text(title, "Название специализации не может быть пустым")
        self.__allowed_categories = frozenset(
            require_text(category, "Категория не может быть пустой").casefold() for category in allowed_categories
        )
        if not self.__allowed_categories:
            raise ValueError("Специализация должна разрешать хотя бы одну категорию")
        if not isinstance(certification_level, int) or not 0 <= certification_level <= self.MAX_CERTIFICATION_LEVEL:
            raise ValueError(f"Уровень сертификации должен быть от 0 до {self.MAX_CERTIFICATION_LEVEL}")
        if not isinstance(years_required, int) or years_required < 0:
            raise ValueError("Требуемый стаж не может быть отрицательным")
        self.__certification_level = certification_level
        self.__years_required = years_required

    @property
    def title(self):
        return self.__title

    @property
    def allowed_categories(self):
        return tuple(sorted(self.__allowed_categories))

    @property
    def certification_level(self):
        return self.__certification_level

    @property
    def years_required(self):
        return self.__years_required

    def allows(self, category):
        return str(category).strip().casefold() in self.__allowed_categories

    def is_certified(self):
        return self.certification_level > 0

    def experience_requirement_met(self, years):
        return years >= self.years_required
