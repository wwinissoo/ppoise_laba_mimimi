from fitness.exceptions import EntityNotFoundError, InvalidValueError
from fitness.users.user import User
from fitness.validation import ensure_instance, ensure_text
from fitness.workouts.template_item import TemplateItem
from fitness.workouts.workout import Workout


class WorkoutTemplate:
    """Переиспользуемый набор упражнений для определённого уровня подготовки."""

    LEVELS = ("новичок", "средний", "продвинутый")

    def __init__(self, name, level):
        self._name = ensure_text(name, "название шаблона")
        if level not in self.LEVELS:
            raise InvalidValueError(f"Уровень должен быть одним из: {', '.join(self.LEVELS)}")
        self._level = level
        self._items = []

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def items(self):
        return tuple(self._items)

    def add_item(self, item):
        self._items.append(ensure_instance(item, TemplateItem, "пункт шаблона"))
        return item

    def remove_item(self, exercise_name):
        for item in self._items:
            if item.exercise.name.casefold() == exercise_name.casefold():
                self._items.remove(item)
                return item
        raise EntityNotFoundError(f"В шаблоне нет упражнения «{exercise_name}»")

    def estimated_duration(self):
        return round(sum(item.estimated_minutes() for item in self._items), 1)

    def target_muscles(self):
        return {muscle for item in self._items for muscle in item.exercise.involved_muscles()}

    def instantiate(self, user, planned_start):
        ensure_instance(user, User, "пользователь")
        if not self._items:
            raise InvalidValueError("Шаблон не содержит упражнений")
        workout = Workout(self._name, user, planned_start)
        for item in self._items:
            workout.add_entry(item.to_entry())
        return workout
