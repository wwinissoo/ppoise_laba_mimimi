class CookingInstruction:
    """Объект предметной области: CookingInstruction."""

    def __init__(self, title, text, difficulty, safety_note):
        self.__title = title
        self.__text = text
        self.__difficulty = difficulty
        self.__safety_note = safety_note


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
        return self.text[:limit]

    def has_safety_warning(self):
        return bool(self.safety_note.strip())

