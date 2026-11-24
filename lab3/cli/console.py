"""Интерактивное меню: только ввод/вывод, вся логика — в FitnessTracker."""

from datetime import datetime

from fitness.application import FitnessTracker
from fitness.exceptions import FitnessTrackerError
from fitness.exercises import (
    BalanceExercise,
    CardioExercise,
    ExerciseLibrary,
    FlexibilityExercise,
    MuscleGroup,
    StrengthExercise,
)
from fitness.nutrition import Food, FoodPortion, Meal
from fitness.users import BodyMeasurement

EXIT_CHOICE = "0"
YES_ANSWER = "д"
DATE_FORMAT = "%Y-%m-%d"
HANDLED_ERRORS = (FitnessTrackerError, ValueError, TypeError, LookupError)


def create_library():
    """Стартовый набор упражнений, доступный сразу после запуска."""
    chest = MuscleGroup("Грудь", MuscleGroup.UPPER)
    legs = MuscleGroup("Ноги", MuscleGroup.LOWER, 72)
    back = MuscleGroup("Спина", MuscleGroup.UPPER)
    shoulders = MuscleGroup("Плечи", MuscleGroup.UPPER)
    arms = MuscleGroup("Руки", MuscleGroup.UPPER, 36)
    core = MuscleGroup("Пресс", MuscleGroup.CORE, 24)
    exercises = [
        StrengthExercise("Жим лёжа", chest, 3, compound=True),
        StrengthExercise("Приседания", legs, 3, compound=True, secondary_muscles=[back]),
        StrengthExercise("Становая тяга", back, 4, compound=True, secondary_muscles=[legs]),
        StrengthExercise("Жим стоя", shoulders, 3, compound=True, secondary_muscles=[arms]),
        StrengthExercise("Подтягивания", back, 4, compound=True, secondary_muscles=[arms]),
        StrengthExercise("Отжимания", chest, 2, compound=True, secondary_muscles=[arms]),
        StrengthExercise("Выпады", legs, 2, compound=True),
        StrengthExercise("Сгибание рук с гантелями", arms, 1),
        StrengthExercise("Разведение гантелей в стороны", shoulders, 2),
        StrengthExercise("Скручивания", core, 1),
        StrengthExercise("Подъём ног в висе", core, 3),
        CardioExercise("Бег на дорожке", legs, 2),
        CardioExercise("Ходьба", legs, 1, met_value=3.5),
        CardioExercise("Велотренажёр", legs, 1, met_value=7.0),
        CardioExercise("Скакалка", legs, 2, met_value=11.0, impact=CardioExercise.HIGH_IMPACT),
        CardioExercise("Гребной тренажёр", back, 2, met_value=7.0, secondary_muscles=[arms]),
        FlexibilityExercise("Наклон к ногам", back, 1, 30),
        FlexibilityExercise("Бабочка", legs, 1, 30),
        FlexibilityExercise("Растяжка плеч", shoulders, 1, 20),
        FlexibilityExercise("Кобра", core, 1, 20, bilateral=False),
        BalanceExercise("Ласточка", legs, 2),
        BalanceExercise("Стойка на одной ноге", legs, 1),
    ]
    library = ExerciseLibrary()
    for exercise in exercises:
        library.add(exercise)
    return library


class FitnessConsole:
    """Консольное меню основных сценариев приложения."""

    def __init__(self, tracker=None, read=None, write=None, clock=None):
        self.tracker = tracker or FitnessTracker(library=create_library())
        self._read = read or input
        self._write = write or print
        self._clock = clock or datetime.now
        self._actions = {
            "1": ("Регистрация", self.register),
            "2": ("Вход", self.login),
            "3": ("Добавить замер тела", self.add_measurement),
            "4": ("Записать тренировку", self.record_workout),
            "5": ("Записать приём пищи", self.record_meal),
            "6": ("Отчёт за неделю", self.show_report),
            "7": ("Библиотека упражнений", self.show_library),
            "8": ("Уведомления", self.show_notifications),
            "9": ("Выйти из аккаунта", self.logout),
        }

    def _ask(self, prompt):
        return self._read(prompt).strip()

    def _ask_number(self, prompt):
        answer = self._ask(prompt).replace(",", ".")
        try:
            return float(answer)
        except ValueError:
            raise ValueError(f"Нужно ввести число, получено «{answer}»") from None

    def _ask_int(self, prompt):
        number = self._ask_number(prompt)
        if not number.is_integer():
            raise ValueError("Нужно ввести целое число")
        return int(number)

    def _ask_date(self, prompt):
        answer = self._ask(prompt)
        try:
            return datetime.strptime(answer, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f"Дата должна быть в формате ГГГГ-ММ-ДД, получено «{answer}»") from None

    def show_menu(self):
        user = self.tracker.current_user
        self._write(f"\n=== Фитнес-трекер ({user.username if user else 'гость'}) ===")
        for key, (title, _) in self._actions.items():
            self._write(f"{key}. {title}")
        self._write(f"{EXIT_CHOICE}. Выход")

    def run(self):
        while True:
            self.show_menu()
            choice = self._ask("Выберите пункт: ")
            if choice == EXIT_CHOICE:
                self._write("До встречи!")
                return
            self.handle(choice)

    def handle(self, choice):
        action = self._actions.get(choice)
        if action is None:
            self._write("Неизвестный пункт меню")
            return
        try:
            action[1]()
        except HANDLED_ERRORS as error:
            self._write(f"Ошибка: {error}")

    def register(self):
        username = self._ask("Логин: ")
        email = self._ask("E-mail: ")
        password = self._ask("Пароль: ")
        birth_date = self._ask_date("Дата рождения (ГГГГ-ММ-ДД): ")
        gender = self._ask("Пол (м/ж): ")
        user = self.tracker.register_user(username, email, password, birth_date, gender)
        self._write(f"Пользователь {user.username} зарегистрирован")

    def login(self):
        user = self.tracker.login(self._ask("Логин: "), self._ask("Пароль: "))
        self._write(f"Добро пожаловать, {user.username}!")

    def logout(self):
        self.tracker.logout()
        self._write("Вы вышли из аккаунта")

    def add_measurement(self):
        self.tracker.require_login()
        weight = self._ask_number("Вес, кг: ")
        height = self._ask_number("Рост, см: ")
        measurement = BodyMeasurement(self._clock().date(), weight, height)
        self.tracker.record_measurement(measurement)
        self._write(f"ИМТ {measurement.bmi()} — {measurement.bmi_category()}")

    def record_workout(self):
        self.tracker.require_login()
        workout = self.tracker.plan_workout(self._ask("Название тренировки: "), self._clock())
        while True:
            name = self._ask("Упражнение: ")
            reps = self._ask_int("Повторения: ")
            weight = self._ask_number("Вес, кг: ")
            rpe = self._ask_number("Тяжесть RPE (1-10): ")
            self.tracker.log_set(workout, name, reps, weight, rpe)
            if self._ask("Ещё подход? (д/н): ").lower() != YES_ANSWER:
                break
        self.tracker.start_workout(workout, workout.planned_start)
        unlocked = self.tracker.finish_workout(workout, self._clock())
        self._write(
            f"Тренировка сохранена: {workout.completed_sets_count()} подходов, объём {workout.total_volume()} кг"
        )
        for achievement in unlocked:
            self._write(f"Получено достижение: {achievement.title}")

    def record_meal(self):
        self.tracker.require_login()
        meal = Meal(self._ask("Приём пищи (завтрак/обед/ужин/перекус): "), self._clock())
        food = Food(
            self._ask("Продукт: "),
            self._ask_number("Ккал на 100 г: "),
            self._ask_number("Белки на 100 г: "),
            self._ask_number("Жиры на 100 г: "),
            self._ask_number("Углеводы на 100 г: "),
        )
        meal.add_portion(FoodPortion(food, self._ask_number("Граммы: ")))
        self.tracker.log_meal(meal)
        diary = self.tracker.diary_for(meal.eaten_at.date())
        self._write(f"Съедено {diary.total_calories()} ккал, осталось {diary.remaining_calories()} ккал")

    def show_report(self):
        report = self.tracker.progress_report(self._clock().date())
        self._write(report.summary())
        self._write(
            f"Серия: {self.tracker.streak().current_streak} дн., очки: {self.tracker.achievements().total_points()}"
        )

    def show_library(self):
        for exercise in self.tracker.library.exercises:
            self._write(f"- {exercise.describe()}")

    def show_notifications(self):
        center = self.tracker.notifications()
        if not center.notifications:
            self._write("Уведомлений нет")
        for item in center.notifications:
            self._write(f"[{'x' if item.read else ' '}] {item.title}: {item.body}")
        center.mark_all_read()
