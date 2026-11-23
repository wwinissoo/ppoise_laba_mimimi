"""Фасад приложения: связывает пользователей, тренировки, питание, цели и уведомления."""

from datetime import timedelta

from fitness.exceptions import DuplicateEntityError, EntityNotFoundError, InvalidCredentialsError
from fitness.exercises import ExerciseLibrary
from fitness.goals import Achievement, AchievementBoard, FitnessGoal, StreakTracker, StrengthGoal, WeightGoal
from fitness.nutrition import CalorieCalculator, Meal, NutritionDiary
from fitness.reports import Notification, NotificationCenter, ProgressReport
from fitness.users import BodyMeasurement, PasswordPolicy, User
from fitness.validation import ensure_instance, ensure_text
from fitness.workouts import ExerciseSet, Workout, WorkoutEntry

WORKOUTS_METRIC = "тренировки"
STREAK_METRIC = "серия"
DEFAULT_ACHIEVEMENTS = (
    ("FIRST", "Первая тренировка", WORKOUTS_METRIC, 1, 10),
    ("TEN", "Десять тренировок", WORKOUTS_METRIC, 10, 50),
    ("STREAK7", "Неделя без пропусков", STREAK_METRIC, 7, 70),
)


class FitnessTracker:
    """Сервис приложения; всё состояние хранится в памяти текущего запуска."""

    def __init__(self, password_policy=None, library=None, calculator=None):
        self._password_policy = ensure_instance(password_policy or PasswordPolicy(), PasswordPolicy, "политика")
        self._library = ensure_instance(library or ExerciseLibrary(), ExerciseLibrary, "библиотека")
        self._calculator = ensure_instance(calculator or CalorieCalculator(), CalorieCalculator, "калькулятор")
        self._users = {}
        self._current_user = None
        self._workouts = {}
        self._diaries = {}
        self._goals = {}
        self._streaks = {}
        self._boards = {}
        self._centers = {}

    @property
    def library(self):
        return self._library

    @property
    def calculator(self):
        return self._calculator

    @property
    def users(self):
        return tuple(self._users.values())

    @property
    def current_user(self):
        return self._current_user

    @staticmethod
    def _key(username):
        return ensure_text(username, "логин").casefold()

    def require_login(self):
        if self._current_user is None:
            raise InvalidCredentialsError("Сначала войдите в аккаунт")
        return self._current_user

    def register_user(self, username, email, password, birth_date, gender):
        key = self._key(username)
        if key in self._users:
            raise DuplicateEntityError(f"Логин «{username}» уже занят")
        user = User.register(username, email, password, birth_date, gender, self._password_policy)
        board = AchievementBoard(user)
        for spec in DEFAULT_ACHIEVEMENTS:
            board.add(Achievement(*spec))
        self._users[key] = user
        self._workouts[key], self._goals[key] = [], []
        self._streaks[key] = StreakTracker("Тренировки")
        self._boards[key] = board
        self._centers[key] = NotificationCenter(user)
        return user

    def login(self, username, password):
        user = self._users.get(self._key(username))
        if user is None or not user.verify_password(password):
            raise InvalidCredentialsError("Неверный логин или пароль")
        self._current_user = user
        return user

    def logout(self):
        self.require_login()
        self._current_user = None

    def get_user(self, username):
        user = self._users.get(self._key(username))
        if user is None:
            raise EntityNotFoundError(f"Пользователь «{username}» не найден")
        return user

    def _state(self, registry):
        return registry[self._key(self.require_login().username)]

    def workouts(self):
        return tuple(self._state(self._workouts))

    def goals(self):
        return tuple(self._state(self._goals))

    def streak(self):
        return self._state(self._streaks)

    def achievements(self):
        return self._state(self._boards)

    def notifications(self):
        return self._state(self._centers)

    def record_measurement(self, measurement):
        user = self.require_login()
        ensure_instance(measurement, BodyMeasurement, "замер")
        user.add_measurement(measurement)
        for goal in self.goals():
            if isinstance(goal, WeightGoal) and goal.status == FitnessGoal.ACTIVE:
                goal.record_measurement(measurement)
        return measurement

    def add_goal(self, goal):
        self._state(self._goals).append(ensure_instance(goal, FitnessGoal, "цель"))
        return goal

    def plan_workout(self, title, planned_start):
        workout = Workout(title, self.require_login(), planned_start)
        self._state(self._workouts).append(workout)
        return workout

    def log_set(self, workout, exercise_name, reps, weight_kg, rpe):
        """Добавляет выполненный подход; запись упражнения создаётся при первом подходе."""
        ensure_instance(workout, Workout, "тренировка")
        exercise = self._library.get(exercise_name)
        entry = workout.find_entry(exercise.name) or workout.add_entry(WorkoutEntry(exercise))
        exercise_set = entry.add_set(ExerciseSet(reps, weight_kg))
        exercise_set.complete(rpe)
        for goal in self.goals():
            if isinstance(goal, StrengthGoal) and goal.exercise is exercise and goal.status == FitnessGoal.ACTIVE:
                goal.record_set(exercise, exercise_set)
        return exercise_set

    def start_workout(self, workout, now):
        ensure_instance(workout, Workout, "тренировка").start(now)
        return workout

    def finish_workout(self, workout, now):
        """Завершает тренировку, продлевает серию и возвращает новые достижения."""
        ensure_instance(workout, Workout, "тренировка").finish(now)
        streak = self.streak().register(now.date())
        completed = sum(1 for item in self.workouts() if item.status == Workout.COMPLETED)
        board = self.achievements()
        unlocked = board.evaluate(WORKOUTS_METRIC, completed, now) + board.evaluate(STREAK_METRIC, streak, now)
        message = f"«{workout.title}»: {workout.duration_minutes()} мин, объём {workout.total_volume()} кг"
        self.notifications().push(Notification("Тренировка завершена", message, now))
        for achievement in unlocked:
            self.notifications().push(Notification("Новое достижение", achievement.title, now))
        return unlocked

    def diary_for(self, day, goal="поддержание"):
        user = self.require_login()
        key = (self._key(user.username), day)
        if key not in self._diaries:
            target = self._calculator.calorie_target(user, goal, today=day)
            self._diaries[key] = NutritionDiary(user, day, target)
        return self._diaries[key]

    def log_meal(self, meal, goal="поддержание"):
        ensure_instance(meal, Meal, "приём пищи")
        return self.diary_for(meal.eaten_at.date(), goal).add_meal(meal)

    def progress_report(self, period_end, days=7):
        start = period_end - timedelta(days=days - 1)
        return ProgressReport(self.require_login(), start, period_end, self.workouts())
