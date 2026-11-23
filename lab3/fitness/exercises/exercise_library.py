from fitness.exceptions import DuplicateEntityError, EntityNotFoundError, InjuryRiskError
from fitness.exercises.exercise import Exercise
from fitness.validation import ensure_instance, ensure_text


class ExerciseLibrary:
    """Справочник упражнений приложения."""

    def __init__(self, title="Библиотека упражнений"):
        self._title = ensure_text(title, "название библиотеки")
        self._exercises = {}

    @property
    def title(self):
        return self._title

    @property
    def exercises(self):
        return tuple(self._exercises.values())

    @staticmethod
    def _key(name):
        return name.strip().casefold()

    def add(self, exercise):
        ensure_instance(exercise, Exercise, "упражнение")
        key = self._key(exercise.name)
        if key in self._exercises:
            raise DuplicateEntityError(f"Упражнение «{exercise.name}» уже есть в библиотеке")
        self._exercises[key] = exercise
        return exercise

    def get(self, name):
        exercise = self._exercises.get(self._key(ensure_text(name, "название упражнения")))
        if exercise is None:
            raise EntityNotFoundError(f"Упражнение «{name}» не найдено")
        return exercise

    def remove(self, name):
        return self._exercises.pop(self._key(self.get(name).name))

    def search(self, text):
        query = ensure_text(text, "поисковый запрос").casefold()
        return [item for item in self._exercises.values() if query in item.name.casefold()]

    def find_by_muscle(self, muscle):
        return [item for item in self._exercises.values() if item.targets(muscle)]

    def find_by_equipment(self, equipment):
        return [item for item in self._exercises.values() if item.requires(equipment)]

    def find_for_level(self, level):
        return [item for item in self._exercises.values() if item.suits_level(level)]

    def safe_for(self, health_profile):
        safe = []
        for exercise in self._exercises.values():
            try:
                health_profile.check_exercise_allowed(exercise)
            except InjuryRiskError:
                continue
            safe.append(exercise)
        return safe
