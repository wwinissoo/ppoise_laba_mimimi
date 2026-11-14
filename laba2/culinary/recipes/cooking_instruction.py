from culinary.validation import require_text


class CookingInstruction:
    """Технологическая инструкция с уровнем сложности и предупреждением о безопасности."""

    DIFFICULTIES = ("лёгкая", "средняя", "сложная")

    def __init__(self, title, text, difficulty, safety_note=""):
        self.__title = require_text(title, "Название инструкции не может быть пустым")
        self.__text = require_text(text, "Текст инструкции не может быть пустым")
        if difficulty not in self.DIFFICULTIES:
            raise ValueError(f"Сложность должна быть одной из: {', '.join(self.DIFFICULTIES)}")
        self.__difficulty = difficulty
        self.__safety_note = str(safety_note or "").strip()

    @property
    def title(self):
        return self.__title

    @property
    def text(self):
        return self.__text

    @property
    def difficulty(self):
        return self.__difficulty

    @property
    def safety_note(self):
        return self.__safety_note

    def validate_text(self):
        return bool(self.text.strip())

    def shorten(self, limit):
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Длина сокращения должна быть положительной")
        return self.text if len(self.text) <= limit else self.text[:limit].rstrip() + "…"

    def has_safety_warning(self):
        return bool(self.safety_note)
