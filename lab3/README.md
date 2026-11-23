# Lab 2 — Object model "Fitness Tracking Application"

A Python console application for tracking workouts, activity, nutrition, goals and fitness-club visits.
The `fitness` package contains the domain object model, `cli` the console interface and `main.py` the entry point.

## Running

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python main.py            # console menu
pytest                    # tests + coverage report (90 % threshold, branch coverage)
black --check . && flake8 # code style and static analysis
python build.py           # build dist/fitness-tracker.pyz
```

## CI/CD

GitHub Actions pipeline: `.github/workflows/lab3.yaml` in the repository root (runs on push to `main`/`dev` and on pull requests that touch `lab3/`, and manually):

1. **lint** — `black --check .` and `flake8`;
2. **test** — `pytest` with coverage (90 % threshold) on Python 3.10–3.13; the `coverage.xml` report is stored as an artifact;
3. **build** — after lint and test succeed, builds `dist/fitness-tracker.pyz`, checks that it starts and publishes it as an artifact.

## Structure

```text
(repository root) .github/workflows/lab3.yaml  CI/CD pipeline
fitness/
  application.py   FitnessTracker — application facade
  validation.py    shared input validation functions
  exceptions/      custom exception hierarchy (one file per exception)
  users/  exercises/  workouts/  tracking/  nutrition/  goals/  gym/  reports/
                   each class lives in its own file (snake_case of the class name),
                   package constants are in constants.py, the public API is in __init__.py
cli/console.py     FitnessConsole — console menu (input/output only)
tests/             pytest tests for every package, the CLI and the facade
```

## Implementation principles

- Encapsulation: state is kept in private fields such as `_name`; the outside world gets read-only properties and immutable tuples.
- Input validation is centralised in `fitness/validation.py`; domain errors are custom exceptions.
- Inheritance is used where behaviour is shared: `Exercise` → `StrengthExercise`/`CardioExercise`/…, `Activity` → `RunActivity`/…, `FitnessGoal` → `WeightGoal`/….
- State machines (`Workout`, `Membership`, `TrainingSession`, `FitnessGoal`) forbid invalid transitions.
- Passwords are stored only as a salted PBKDF2 hash and compared with `hmac.compare_digest`.
- No "magic numbers": coefficients and thresholds are named constants.
- The CLI contains no business logic and receives its dependencies (input, output, clock) through the constructor, which makes it easy to test.

## Quantitative metrics

Counted automatically by parsing the AST of the `fitness` package.

| Requirement | Minimum | Actual | How it was counted |
|---|---|---|---|
| Interrelated domain classes | 50 | **64** (all 64 are linked) | classes of the `fitness` package, exceptions excluded |
| Fields | 150 | **255** | instance attributes created in `__init__` |
| Unique behaviours | 100 | **318** | public methods, excluding property getters and `__dunder__` methods |
| Associations | 30 | **77** | "class → other class" pairs in a field or method parameter |
| Custom exceptions | 12 | **22** | subclasses of `FitnessTrackerError` |
| Test coverage | 90 % | **100 %** | `pytest` with `--cov-branch` |

### Class connectivity

Each of the 64 domain classes takes part in at least one association (as the owner of a field/parameter or as the type of another class's field/parameter). There are no isolated classes. Number of links per class:

| Class | Links | Linked with |
|---|---|---|
| `FitnessTracker` | 9 | BodyMeasurement, CalorieCalculator, ExerciseLibrary, FitnessGoal, Meal, PasswordPolicy, StrengthGoal, WeightGoal, Workout |
| `Exercise` | 5 | Equipment, ExerciseLibrary, MuscleGroup, TemplateItem, WorkoutEntry |
| `StrengthExercise` | 3 | RestTimer, StrengthGoal, WorkoutEntry |
| `CardioExercise` | 1 | Route |
| `FlexibilityExercise` | 1 | Injury |
| `BalanceExercise` | 1 | HealthProfile |
| `ExerciseLibrary` | 2 | Exercise, FitnessTracker |
| `MuscleGroup` | 2 | Exercise, Injury |
| `Equipment` | 1 | Exercise |
| `Achievement` | 1 | AchievementBoard |
| `AchievementBoard` | 2 | Achievement, User |
| `ChallengeEntry` | 1 | User |
| `Challenge` | 1 | User |
| `FitnessGoal` | 1 | FitnessTracker |
| `WeightGoal` | 2 | BodyMeasurement, FitnessTracker |
| `DistanceGoal` | 1 | Activity |
| `StrengthGoal` | 3 | ExerciseSet, FitnessTracker, StrengthExercise |
| `StreakTracker` | 1 | Workout |
| `Locker` | 2 | User, Visit |
| `Visit` | 2 | Locker, User |
| `Gym` | 1 | Membership |
| `GroupClass` | 2 | Membership, Trainer |
| `MembershipPlan` | 1 | Membership |
| `Payment` | 1 | Membership |
| `Membership` | 5 | GroupClass, Gym, MembershipPlan, Payment, User |
| `CalorieCalculator` | 3 | BodyMeasurement, FitnessTracker, User |
| `MacroTargets` | 1 | NutritionDiary |
| `NutritionDiary` | 4 | MacroTargets, Meal, Supplement, User |
| `Food` | 1 | FoodPortion |
| `FoodPortion` | 2 | Food, Meal |
| `Meal` | 3 | FitnessTracker, FoodPortion, NutritionDiary |
| `Supplement` | 1 | NutritionDiary |
| `Reminder` | 1 | NotificationCenter |
| `Notification` | 1 | NotificationCenter |
| `NotificationCenter` | 3 | Notification, Reminder, User |
| `ProgressReport` | 2 | User, Workout |
| `Activity` | 2 | DistanceGoal, User |
| `RunActivity` | 1 | Route |
| `CyclingActivity` | 1 | Route |
| `SwimmingActivity` | 1 | WearableDevice |
| `DailyActivity` | 2 | SleepRecord, WearableDevice |
| `SleepRecord` | 1 | DailyActivity |
| `WearableDevice` | 4 | DailyActivity, HeartRateMonitor, SwimmingActivity, User |
| `GpsPoint` | 1 | Route |
| `Route` | 4 | CardioExercise, CyclingActivity, GpsPoint, RunActivity |
| `HeartRateSample` | 1 | HeartRateMonitor |
| `HeartRateZone` | 1 | HeartRateMonitor |
| `HeartRateMonitor` | 3 | HeartRateSample, HeartRateZone, WearableDevice |
| `BodyMeasurement` | 4 | CalorieCalculator, FitnessTracker, User, WeightGoal |
| `Injury` | 3 | FlexibilityExercise, HealthProfile, MuscleGroup |
| `HealthProfile` | 3 | BalanceExercise, Injury, User |
| `PasswordPolicy` | 2 | FitnessTracker, User |
| `Certification` | 1 | Trainer |
| `Trainer` | 4 | Certification, GroupClass, TrainingSession, User |
| `UserSettings` | 1 | User |
| `User` | 20 | AchievementBoard, Activity, BodyMeasurement, CalorieCalculator, Challenge, ChallengeEntry, HealthProfile, Locker, Membership, NotificationCenter, NutritionDiary, PasswordPolicy, ProgressReport, Trainer, TrainingSession, UserSettings, Visit, WearableDevice, Workout, WorkoutTemplate |
| `TemplateItem` | 2 | Exercise, WorkoutTemplate |
| `WorkoutTemplate` | 3 | TemplateItem, User, WorkoutPlan |
| `WorkoutPlan` | 1 | WorkoutTemplate |
| `TrainingSession` | 2 | Trainer, User |
| `RestTimer` | 1 | StrengthExercise |
| `ExerciseSet` | 2 | StrengthGoal, WorkoutEntry |
| `WorkoutEntry` | 4 | Exercise, ExerciseSet, StrengthExercise, Workout |
| `Workout` | 5 | FitnessTracker, ProgressReport, StreakTracker, User, WorkoutEntry |

## Exceptions

There are **22** custom exception classes (at least 12 are required). All of them inherit from `FitnessTrackerError`.

| Exception | Parent | Raised when |
|---|---|---|
| `FitnessTrackerError` | `Exception` | Root of the hierarchy: any domain error. |
| `InvalidValueError` | `FitnessTrackerError`, `ValueError` | Invalid input value (empty string, negative number, etc.). |
| `InvalidMeasurementError` | `InvalidValueError` | Physically impossible body measurement or sensor reading. |
| `AuthenticationError` | `FitnessTrackerError` | General login and password-management error. |
| `WeakPasswordError` | `AuthenticationError` | The password does not satisfy the complexity policy. |
| `InvalidCredentialsError` | `AuthenticationError` | Wrong username/password pair. |
| `EntityNotFoundError` | `FitnessTrackerError`, `LookupError` | The requested object (user, exercise, workout) was not found. |
| `DuplicateEntityError` | `FitnessTrackerError` | An object with this identifier is already registered. |
| `WorkoutStateError` | `FitnessTrackerError` | Invalid workout status transition or an action in the wrong status. |
| `InjuryRiskError` | `FitnessTrackerError` | The exercise is contraindicated because of an active injury. |
| `GoalStateError` | `FitnessTrackerError` | The action is impossible in the goal's current status. |
| `DeviceError` | `FitnessTrackerError` | Wearable device malfunction. |
| `DevicePairingError` | `DeviceError` | The device is not paired or is already paired with another user. |
| `LowBatteryError` | `DeviceError` | Not enough battery for the operation. |
| `MembershipError` | `FitnessTrackerError` | General membership error. |
| `MembershipExpiredError` | `MembershipError` | The membership is inactive or has expired. |
| `MembershipFrozenError` | `MembershipError` | The membership is frozen or the freeze limit is exhausted. |
| `PaymentDeclinedError` | `FitnessTrackerError` | Payment declined: wrong amount, repeated payment or refund without payment. |
| `CapacityExceededError` | `FitnessTrackerError` | Capacity of the gym, group class or lockers exceeded. |
| `ScheduleConflictError` | `FitnessTrackerError` | Overlapping classes, sessions or reminders. |
| `NutritionLimitError` | `FitnessTrackerError` | The daily limit of a supplement or nutrition is exceeded. |
| `ChallengeError` | `FitnessTrackerError` | Challenge rules violated (not a participant, challenge inactive, etc.). |

## Classes

For every class the fields (instance attributes), behaviour methods and associations are listed. Fields are available through same-named properties without the underscore.

### Core: facade, validation, exceptions

#### `FitnessTracker`

Application service; all state lives in memory for the current run. File: `fitness/application.py`.

- **Fields:** `_password_policy`, `_library`, `_calculator`, `_users`, `_current_user`, `_workouts`, `_diaries`, `_goals`, `_streaks`, `_boards`, `_centers`
- **Methods:**
  - `require_login()` — returns the logged-in user or raises InvalidCredentialsError
  - `register_user(username, email, password, birth_date, gender)` — registers a user and creates their streak, achievement board and notification center
  - `login(username, password)` — checks the username and password and opens a session
  - `logout()` — ends the user's session
  - `get_user(username)` — looks a user up by username
  - `workouts()` — workouts of the current user
  - `goals()` — goals of the current user
  - `streak()` — the current user's streak of training days
  - `achievements()` — the current user's achievement board
  - `notifications()` — the current user's notification center
  - `record_measurement(measurement)` — saves a body measurement and updates active weight goals
  - `add_goal(goal)` — adds a goal for the user
  - `plan_workout(title, planned_start)` — plans a new workout
  - `log_set(workout, exercise_name, reps, weight_kg, rpe)` — records a completed set and updates strength goals
  - `start_workout(workout, now)` — starts a workout
  - `finish_workout(workout, now)` — finishes a workout, extends the streak, awards achievements and notifications
  - `diary_for(day, goal)` — nutrition diary for a day with the calorie target from the calculator
  - `log_meal(meal, goal)` — records a meal in the diary of the right day
  - `progress_report(period_end, days)` — progress report for the last N days
- **Associations:** `BodyMeasurement` (parameter), `CalorieCalculator` (field), `ExerciseLibrary` (field), `FitnessGoal` (parameter), `Meal` (parameter), `PasswordPolicy` (field), `StrengthGoal` (parameter), `WeightGoal` (parameter), `Workout` (parameter)

### users — users, health, security, trainers

#### `BodyMeasurement`

Body measurement on a given date. File: `fitness/users/body_measurement.py`.

- **Fields:** `_measured_on`, `_weight_kg`, `_height_cm`, `_body_fat_percent`, `_waist_cm`
- **Constants:** `UNDERWEIGHT_LIMIT`, `NORMAL_LIMIT`, `OVERWEIGHT_LIMIT`, `CM_IN_METER`
- **Methods:**
  - `bmi()` — body mass index
  - `bmi_category()` — BMI category
  - `lean_mass_kg()` — lean body mass
  - `waist_to_height_ratio()` — waist-to-height ratio
  - `weight_difference(earlier)` — weight difference from another measurement

#### `Injury`

An injury that limits the load on a muscle group. File: `fitness/users/injury.py`.

- **Fields:** `_muscle_group`, `_severity`, `_occurred_on`, `_description`, `_recovered_on`
- **Constants:** `MILD`, `MODERATE`, `SEVERE`, `RECOVERY_DAYS`
- **Methods:**
  - `is_active()` — has the injury not healed yet?
  - `mark_recovered(recovered_on)` — marks the recovery
  - `affects(muscle_group)` — whether it affects the muscle group
  - `allows_stretching(exercise)` — whether stretching (`FlexibilityExercise`) is allowed with this injury
  - `expected_recovery_date()` — expected recovery date based on severity
- **Associations:** `FlexibilityExercise` (parameter), `MuscleGroup` (field)

#### `HealthProfile`

The user's medical indicators and restrictions. File: `fitness/users/health_profile.py`.

- **Fields:** `_resting_heart_rate`, `_systolic_pressure`, `_diastolic_pressure`, `_injuries`, `_chronic_conditions`
- **Constants:** `HYPERTENSION_SYSTOLIC`, `HYPERTENSION_DIASTOLIC`
- **Methods:**
  - `add_injury(injury)` — adds an injury
  - `add_condition(condition)` — adds a chronic condition
  - `active_injuries()` — injuries that have not healed
  - `is_hypertensive()` — whether the user has hypertension
  - `update_pressure(systolic, diastolic)` — updates blood pressure
  - `max_heart_rate(age)` — maximum heart rate by age
  - `heart_rate_reserve(age)` — heart-rate reserve (Karvonen)
  - `check_exercise_allowed(exercise)` — forbids exercises that load injured muscles
  - `needs_spotter(exercise)` — whether a spotter is needed for a balance exercise (`BalanceExercise`)
- **Associations:** `BalanceExercise` (parameter), `Injury` (parameter)

#### `PasswordPolicy`

Password complexity rules and salted hashing. File: `fitness/users/password_policy.py`.

- **Fields:** `_min_length`, `_require_digit`, `_require_uppercase`, `_require_special`
- **Constants:** `HASH_ITERATIONS`, `SALT_BYTES`, `SPECIAL_CHARACTERS`
- **Methods:**
  - `find_violations(raw_password)` — list of violated password requirements
  - `validate(raw_password)` — checks the password or raises WeakPasswordError
  - `strength_score(raw_password)` — strength score 0–5
  - `generate_salt()` — random salt
  - `hash_password(raw_password, salt)` — PBKDF2-HMAC-SHA256 hash
  - `matches(raw_password, salt, expected_hash)` — constant-time comparison of a password with a hash

#### `Certification`

A trainer certificate with an expiry date. File: `fitness/users/certification.py`.

- **Fields:** `_title`, `_issuer`, `_valid_until`
- **Methods:**
  - `is_valid(on_date)` — whether the certificate is valid
  - `days_until_expiry(on_date)` — days until it expires

#### `Trainer`

A trainer who leads clients and group classes. File: `fitness/users/trainer.py`.

- **Fields:** `_full_name`, `_specializations`, `_hourly_rate`, `_max_clients`, `_certifications`, `_clients`
- **Methods:**
  - `add_certification(certification)` — adds a certificate
  - `is_certified(on_date)` — whether the trainer has a valid certificate
  - `can_lead(workout_type)` — whether the trainer leads this type of workout
  - `assign_client(user)` — assigns a client, respecting the limit
  - `release_client(user)` — releases a client
  - `session_fee(minutes)` — session price by duration
- **Associations:** `Certification` (parameter), `User` (parameter)

#### `UserSettings`

Units of measurement, weekly target and notifications. File: `fitness/users/user_settings.py`.

- **Fields:** `_unit_system`, `_weekly_workout_target`, `_notifications_enabled`, `_language`
- **Constants:** `METRIC`, `IMPERIAL`, `POUNDS_PER_KG`, `MAX_WEEKLY_WORKOUTS`
- **Methods:**
  - `toggle_notifications()` — turns notifications on/off
  - `switch_unit_system()` — switches between metric and imperial
  - `set_weekly_target(workouts)` — sets the number of workouts per week
  - `format_weight(weight_kg)` — formats a weight in the chosen units

#### `User`

A registered user with a history of body measurements. File: `fitness/users/user.py`.

- **Fields:** `_username`, `_email`, `_password_hash`, `_salt`, `_birth_date`, `_gender`, `_health_profile`, `_settings`, `_measurements`
- **Constants:** `MALE`, `FEMALE`, `GENDERS`, `MIN_AGE`
- **Methods:**
  - `register(username, email, raw_password, birth_date, gender, policy)` — creates a user, validating and hashing the password
  - `age(today)` — age on a date
  - `verify_password(raw_password)` — checks the password
  - `change_password(old_password, new_password, policy)` — changes the password after checking the old one
  - `update_email(email)` — changes the e-mail after format validation
  - `add_measurement(measurement)` — adds a measurement (one per day)
  - `latest_measurement()` — the latest measurement
  - `weight_change()` — weight change from the first measurement to the last
- **Associations:** `BodyMeasurement` (parameter), `HealthProfile` (field), `PasswordPolicy` (parameter), `UserSettings` (field)

### exercises — exercises, muscles, equipment

#### `Exercise`

An exercise with a primary muscle group, difficulty and MET coefficient. File: `fitness/exercises/exercise.py`.

- **Fields:** `_name`, `_primary_muscle`, `_difficulty`, `_met_value`, `_equipment`, `_secondary_muscles`
- **Constants:** `CATEGORY`
- **Methods:**
  - `involved_muscles()` — primary and secondary muscles
  - `targets(muscle)` — checks whether the exercise engages the muscle
  - `requires(equipment)` — checks whether the given equipment is needed
  - `suits_level(level)` — whether the exercise suits the fitness level
  - `is_available()` — whether all equipment is in working order
  - `calories_burned(body_weight_kg, minutes)` — calorie expenditure from MET, weight and duration
  - `describe()` — short text description of the exercise
- **Associations:** `Equipment` (field), `MuscleGroup` (field)

#### `StrengthExercise` (inherits `Exercise`)

A strength exercise with added load. File: `fitness/exercises/strength_exercise.py`.

- **Fields:** `_compound`
- **Constants:** `CATEGORY`, `EPLEY_DIVISOR`, `COMPOUND_REST_SECONDS`, `ISOLATION_REST_SECONDS`
- **Methods:**
  - `estimate_one_rep_max(weight_kg, reps)` — one-rep-max estimate (Epley formula)
  - `recommended_rest_seconds()` — recommended rest between sets
  - `check_load(weight_kg)` — checks whether the equipment can bear the weight

#### `CardioExercise` (inherits `Exercise`)

A cardio load with an impact rating for the joints. File: `fitness/exercises/cardio_exercise.py`.

- **Fields:** `_impact`
- **Constants:** `CATEGORY`, `LOW_IMPACT`, `HIGH_IMPACT`, `MINUTES_PER_HOUR`
- **Methods:**
  - `is_low_impact()` — whether the joint load is low-impact
  - `pace_min_per_km(distance_km, minutes)` — pace, min/km
  - `speed_kmh(distance_km, minutes)` — speed, km/h

#### `FlexibilityExercise` (inherits `Exercise`)

Stretching with a held pose. File: `fitness/exercises/flexibility_exercise.py`.

- **Fields:** `_hold_seconds`, `_bilateral`
- **Constants:** `CATEGORY`
- **Methods:**
  - `total_hold_time(rounds)` — total hold time over the repetitions (both sides counted)
  - `extend_hold(extra_seconds)` — increases the hold time

#### `BalanceExercise` (inherits `Exercise`)

A balance exercise with a support stability level. File: `fitness/exercises/balance_exercise.py`.

- **Fields:** `_stability_level`
- **Constants:** `CATEGORY`, `SUPPORT_THRESHOLD`
- **Methods:**
  - `progress()` — moves to the next stability level
  - `requires_support()` — whether support is needed at the current level

#### `ExerciseLibrary`

The application's exercise catalogue. File: `fitness/exercises/exercise_library.py`.

- **Fields:** `_title`, `_exercises`
- **Methods:**
  - `add(exercise)` — adds an exercise (no duplicates)
  - `get(name)` — gets an exercise by name
  - `remove(name)` — removes an exercise
  - `search(text)` — search by part of the name
  - `find_by_muscle(muscle)` — exercises for a muscle group
  - `find_by_equipment(equipment)` — exercises using the given equipment
  - `find_for_level(level)` — exercises for a fitness level
  - `safe_for(health_profile)` — exercises that are safe given the health profile's injuries
- **Associations:** `Exercise` (parameter)

#### `MuscleGroup`

A muscle group with a post-exercise recovery norm. File: `fitness/exercises/muscle_group.py`.

- **Fields:** `_name`, `_region`, `_recovery_hours`
- **Constants:** `UPPER`, `LOWER`, `CORE`, `REGIONS`
- **Methods:**
  - `is_upper_body()` — whether the group belongs to the upper body
  - `hours_until_recovered(last_trained_at, now)` — hours left until recovery
  - `is_recovered(last_trained_at, now)` — whether the muscle has recovered after training

#### `Equipment`

A machine or free weight with a load limit. File: `fitness/exercises/equipment.py`.

- **Fields:** `_name`, `_category`, `_max_load_kg`, `_adjustable`, `_in_service`
- **Methods:**
  - `can_handle(load_kg)` — whether the equipment can bear the load
  - `put_out_of_service()` — takes the equipment out of service
  - `return_to_service()` — returns the equipment to service

### workouts — workouts, sets, plans, sessions

#### `TemplateItem`

A template item: an exercise with target sets/reps/weight. File: `fitness/workouts/template_item.py`.

- **Fields:** `_exercise`, `_target_sets`, `_target_reps`, `_target_weight_kg`, `_rest_seconds`
- **Methods:**
  - `estimated_minutes()` — time estimate for the exercise
  - `planned_volume()` — planned tonnage
  - `to_entry()` — creates a workout entry with planned sets
- **Associations:** `Exercise` (field)

#### `WorkoutTemplate`

A reusable set of exercises for a given fitness level. File: `fitness/workouts/workout_template.py`.

- **Fields:** `_name`, `_level`, `_items`
- **Constants:** `LEVELS`
- **Methods:**
  - `add_item(item)` — adds a template item
  - `remove_item(exercise_name)` — removes an item by exercise
  - `estimated_duration()` — duration estimate
  - `target_muscles()` — muscles the template works
  - `instantiate(user, planned_start)` — creates a workout from the template
- **Associations:** `TemplateItem` (parameter), `User` (parameter)

#### `WorkoutPlan`

A multi-week plan: a template for each training weekday. File: `fitness/workouts/workout_plan.py`.

- **Fields:** `_name`, `_start_date`, `_weeks`, `_schedule`
- **Methods:**
  - `end_date()` — programme end date
  - `assign(weekday, template)` — assigns a template to a weekday
  - `unassign(weekday)` — removes the template from a weekday
  - `covers(day)` — whether the date falls within the programme
  - `template_for(day)` — template for a date
  - `is_rest_day(day)` — is it a rest day?
  - `sessions_per_week()` — workouts per week
  - `total_sessions()` — workouts over the whole programme
  - `schedule_workout(user, day, start_hour)` — schedules a workout on a date according to the programme
- **Associations:** `WorkoutTemplate` (parameter)

#### `TrainingSession`

A client's booking for a personal training session. File: `fitness/workouts/training_session.py`.

- **Fields:** `_trainer`, `_client`, `_starts_at`, `_duration_minutes`, `_status`
- **Constants:** `BOOKED`, `DONE`, `CANCELLED`, `LATE_CANCEL_HOURS`, `LATE_CANCEL_PENALTY`
- **Methods:**
  - `ends_at()` — end time
  - `fee()` — session price
  - `overlaps(other)` — whether it overlaps with a session of the same trainer or client
  - `reschedule(new_start, other_sessions)` — moves the session without conflicts
  - `complete()` — marks it as held
  - `cancel(now)` — cancels and calculates the late-cancellation penalty
- **Associations:** `Trainer` (field), `User` (field)

#### `RestTimer`

A timer for rest between sets. File: `fitness/workouts/rest_timer.py`.

- **Fields:** `_duration_seconds`, `_elapsed_seconds`, `_running`
- **Methods:**
  - `for_exercise(exercise)` — creates a timer with the recommended rest for a strength exercise (`StrengthExercise`)
  - `start()` — starts the timer
  - `pause()` — pauses it
  - `tick(seconds)` — counts down seconds and returns the remainder
  - `remaining()` — remaining time
  - `is_finished()` — is the rest over?
  - `add_time(seconds)` — adds time
  - `reset()` — resets the timer
- **Associations:** `StrengthExercise` (parameter)

#### `ExerciseSet`

A single set: reps, weight, time and rating of perceived exertion (RPE). File: `fitness/workouts/exercise_set.py`.

- **Fields:** `_reps`, `_weight_kg`, `_duration_seconds`, `_rpe`, `_completed`
- **Constants:** `MIN_RPE`, `MAX_RPE`, `LIGHT_RPE_LIMIT`, `MODERATE_RPE_LIMIT`
- **Methods:**
  - `volume()` — tonnage of the set
  - `complete(rpe)` — marks completion with an RPE rating
  - `intensity_label()` — exertion level by RPE

#### `WorkoutEntry`

An exercise within a workout, with a list of sets. File: `fitness/workouts/workout_entry.py`.

- **Fields:** `_exercise`, `_note`, `_sets`
- **Methods:**
  - `add_set(exercise_set)` — adds a set, checking the load
  - `remove_set(index)` — removes a set by number
  - `completed_sets()` — completed sets
  - `total_volume()` — tonnage of the exercise
  - `total_duration_seconds()` — duration of timed sets
  - `best_set()` — the best set
  - `estimated_one_rep_max()` — 1RM estimate from the best set
- **Associations:** `Exercise` (field), `ExerciseSet` (parameter), `StrengthExercise` (parameter)

#### `Workout`

A user's workout consisting of exercise entries. File: `fitness/workouts/workout.py`.

- **Fields:** `_title`, `_user`, `_planned_start`, `_status`, `_entries`, `_started_at`, `_finished_at`
- **Constants:** `PLANNED`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`, `TRANSITIONS`
- **Methods:**
  - `add_entry(entry)` — adds an exercise, checking injuries
  - `find_entry(exercise_name)` — finds an exercise in the workout
  - `start(now)` — starts the workout
  - `finish(now)` — finishes the workout
  - `cancel()` — cancels the workout
  - `duration_minutes()` — duration
  - `total_volume()` — tonnage of the workout
  - `completed_sets_count()` — number of completed sets
  - `muscles_worked()` — muscles worked
  - `estimate_calories(body_weight_kg)` — calorie expenditure estimate
- **Associations:** `User` (field), `WorkoutEntry` (parameter)

### tracking — activities, GPS, heart rate, sleep, wearables

#### `Activity`

A base activity with a duration and a MET-based calorie estimate. File: `fitness/tracking/activity.py`.

- **Fields:** `_user`, `_started_at`, `_duration_minutes`
- **Constants:** `MET`, `KIND`
- **Methods:**
  - `ends_at()` — end time
  - `overlaps(other)` — whether it overlaps with another activity
  - `distance_km()` — distance (0 for the base activity)
  - `calories_burned(body_weight_kg)` — calorie expenditure from MET
  - `summary()` — short summary
- **Associations:** `User` (field)

#### `RunActivity` (inherits `Activity`)

A run along a GPS route. File: `fitness/tracking/run_activity.py`.

- **Fields:** `_route`
- **Constants:** `MET`, `KIND`, `RIEGEL_EXPONENT`
- **Methods:**
  - `distance_km()` — distance along the GPS route
  - `average_pace()` — average pace, min/km
  - `predict_race_minutes(race_km)` — race time prediction (Riegel formula)
- **Associations:** `Route` (field)

#### `CyclingActivity` (inherits `Activity`)

A bike ride along a GPS route. File: `fitness/tracking/cycling_activity.py`.

- **Fields:** `_route`, `_bike_type`
- **Constants:** `MET`, `KIND`, `BIKE_TYPES`
- **Methods:**
  - `distance_km()` — distance along the route
  - `average_speed_kmh()` — average speed
  - `climbing_rate()` — elevation gain per kilometre
- **Associations:** `Route` (field)

#### `SwimmingActivity` (inherits `Activity`)

Swimming in a pool. File: `fitness/tracking/swimming_activity.py`.

- **Fields:** `_pool_length_m`, `_laps`, `_stroke`
- **Constants:** `MET`, `KIND`, `STROKES`, `PACE_DISTANCE_M`
- **Methods:**
  - `distance_meters()` — distance in metres
  - `distance_km()` — distance in kilometres
  - `pace_per_100m()` — pace per 100 m
  - `swolf(strokes_per_lap)` — SWOLF efficiency index

#### `DailyActivity`

Steps, active minutes and floors for a day. File: `fitness/tracking/daily_activity.py`.

- **Fields:** `_day`, `_step_goal`, `_steps`, `_active_minutes`, `_floors`, `_sleep`
- **Methods:**
  - `attach_sleep(sleep)` — attaches the night's sleep (`SleepRecord`) that ended on this day
  - `is_well_recovered()` — whether the user has recovered: enough sleep and not of poor quality
  - `add_steps(steps)` — adds steps
  - `add_active_minutes(minutes)` — adds active minutes
  - `climb_floors(floors)` — adds floors
  - `distance_km(stride_m)` — distance walked based on stride length
  - `goal_progress()` — percentage of the daily step goal
  - `is_goal_reached()` — whether the step goal is reached
- **Associations:** `SleepRecord` (parameter)

#### `SleepRecord`

A night's sleep with phases and awakenings. File: `fitness/tracking/sleep_record.py`.

- **Fields:** `_went_to_bed`, `_woke_up`, `_deep_minutes`, `_rem_minutes`, `_awakenings`
- **Constants:** `GOOD_EFFICIENCY`, `FAIR_EFFICIENCY`, `MAX_GOOD_AWAKENINGS`
- **Methods:**
  - `duration_minutes()` — sleep duration in minutes
  - `duration_hours()` — sleep duration in hours
  - `restorative_percent()` — share of deep and REM sleep
  - `quality_label()` — sleep quality rating
  - `is_sufficient(minimum_hours)` — whether sleep is sufficient

#### `WearableDevice`

A fitness band: pairing, synchronisation, battery and firmware. File: `fitness/tracking/wearable_device.py`.

- **Fields:** `_model`, `_serial_number`, `_firmware_version`, `_battery_percent`, `_paired_user`, `_last_synced_at`
- **Constants:** `FULL_BATTERY`, `SYNC_MIN_BATTERY`, `FIRMWARE_MIN_BATTERY`, `SYNC_DRAIN`, `MEASUREMENT_DRAIN`
- **Methods:**
  - `pair(user)` — pairs the device with a user
  - `unpair()` — unpairs the device
  - `sync_steps(daily_activity, steps, now)` — synchronises steps, draining the battery
  - `measure_heart_rate(monitor, bpm, now)` — measures heart rate and writes it to the monitor
  - `charge(percent)` — charges the device
  - `update_firmware(version)` — updates the firmware to a newer version
  - `needs_sync(now, max_hours)` — whether it is time to synchronise
  - `import_swim(activity, now)` — imports a swim (`SwimmingActivity`) of the paired user and returns the distance
- **Associations:** `DailyActivity` (parameter), `HeartRateMonitor` (parameter), `SwimmingActivity` (parameter), `User` (parameter)

#### `GpsPoint`

A track coordinate with altitude and recording time. File: `fitness/tracking/gps_point.py`.

- **Fields:** `_recorded_at`, `_altitude_m`, `_latitude`, `_longitude`
- **Methods:**
  - `distance_to(other)` — distance to another point (haversine)
  - `seconds_to(other)` — time between points

#### `Route`

A track ordered by time. File: `fitness/tracking/route.py`.

- **Fields:** `_name`, `_points`
- **Methods:**
  - `add_point(point)` — adds a point in chronological order
  - `total_distance_km()` — route length
  - `elevation_gain_m()` — total elevation gain
  - `duration_seconds()` — route duration
  - `is_loop(tolerance_km)` — whether the route is closed
  - `calories_for(exercise, body_weight_kg)` — calories for covering the route with a cardio exercise (`CardioExercise`)
- **Associations:** `CardioExercise` (parameter), `GpsPoint` (parameter)

#### `HeartRateSample`

A single heart-rate measurement. File: `fitness/tracking/heart_rate_sample.py`.

- **Fields:** `_recorded_at`, `_bpm`
- **Constants:** `MIN_BPM`, `MAX_BPM`
- **Methods:**
  - `is_elevated(resting_bpm, margin)` — whether the heart rate is elevated relative to rest

#### `HeartRateZone`

A heart-rate zone as a percentage of maximum heart rate. File: `fitness/tracking/heart_rate_zone.py`.

- **Fields:** `_name`, `_lower_percent`, `_upper_percent`
- **Methods:**
  - `bounds(max_heart_rate)` — zone bounds in bpm
  - `contains(bpm, max_heart_rate)` — whether the heart rate falls in the zone

#### `HeartRateMonitor`

A heart-rate log for an activity with zone analysis. File: `fitness/tracking/heart_rate_monitor.py`.

- **Fields:** `_max_heart_rate`, `_zones`, `_samples`
- **Constants:** `DEFAULT_ZONES`
- **Methods:**
  - `record(sample)` — records a measurement by time
  - `average_bpm()` — average heart rate
  - `peak_bpm()` — peak heart rate
  - `zone_of(bpm)` — zone for a heart-rate value
  - `seconds_in_zone(zone)` — time in a zone
  - `exceeds_safe_limit()` — whether the maximum heart rate is exceeded
- **Associations:** `HeartRateSample` (parameter), `HeartRateZone` (field)

### nutrition — nutrition and calories

#### `CalorieCalculator`

The Mifflin–St Jeor formula with an activity factor. File: `fitness/nutrition/calorie_calculator.py`.

- **Fields:** `_activity_level`
- **Constants:** `ACTIVITY_FACTORS`, `GOAL_ADJUSTMENTS`, `MIN_SAFE_CALORIES`, `GENDER_CONSTANTS`
- **Methods:**
  - `change_activity_level(level)` — changes the activity level
  - `basal_metabolic_rate(user, today, measurement)` — basal metabolic rate (Mifflin–St Jeor)
  - `daily_energy_expenditure(user, today, measurement)` — daily expenditure including activity
  - `calorie_target(user, goal, today, measurement)` — calorie target for a goal, never below the safe minimum
- **Associations:** `BodyMeasurement` (parameter), `User` (parameter)

#### `MacroTargets`

Daily protein, fat and carbohydrate targets in grams. File: `fitness/nutrition/macro_targets.py`.

- **Fields:** `_protein_g`, `_fat_g`, `_carbs_g`
- **Methods:**
  - `from_calories(calories, protein_share, fat_share)` — macro targets from calories and shares
  - `as_dict()` — targets as a dictionary
  - `calories()` — calories of the targets
  - `deviation(actual)` — deviation of the actual intake from the targets
  - `is_balanced(actual, tolerance_percent)` — whether the actual intake is within tolerance

#### `NutritionDiary`

A user's nutrition diary for one day. File: `fitness/nutrition/nutrition_diary.py`.

- **Fields:** `_user`, `_day`, `_calorie_target`, `_meals`, `_water_ml`, `_supplements`
- **Constants:** `WATER_ML_PER_KG`
- **Methods:**
  - `take_supplement(supplement, doses)` — takes a supplement (`Supplement`) with the daily limit enforced and records it in the diary
  - `add_meal(meal)` — adds a meal of this day
  - `drink_water(milliliters)` — records water drunk
  - `total_calories()` — calories eaten during the day
  - `remaining_calories()` — remainder up to the target
  - `is_over_target()` — whether the target is exceeded
  - `total_macros()` — macros for the day
  - `water_goal_ml()` — water target based on the latest weight
  - `macro_report(targets)` — report of deviation from the macro targets
- **Associations:** `MacroTargets` (parameter), `Meal` (parameter), `Supplement` (parameter), `User` (field)

#### `Food`

A food item with calories and macros per 100 g. File: `fitness/nutrition/food.py`.

- **Fields:** `_name`, `_calories_per_100g`, `_protein_g`, `_fat_g`, `_carbs_g`
- **Constants:** `HIGH_PROTEIN_SHARE`
- **Methods:**
  - `nutrients_for(grams)` — calories and macros for a given mass
  - `is_high_protein()` — whether the food is high in protein
  - `grams_for_calories(calories)` — how many grams give the given calories

#### `FoodPortion`

A specific portion of a food in grams. File: `fitness/nutrition/food_portion.py`.

- **Fields:** `_food`, `_grams`
- **Methods:**
  - `nutrients()` — calories and macros of the portion
  - `calories()` — calories of the portion
  - `scaled(factor)` — a new portion multiplied by a factor
- **Associations:** `Food` (field)

#### `Meal`

A meal made of several portions. File: `fitness/nutrition/meal.py`.

- **Fields:** `_meal_type`, `_eaten_at`, `_portions`
- **Constants:** `TYPES`, `MACROS`
- **Methods:**
  - `add_portion(portion)` — adds a portion
  - `remove_food(food_name)` — removes a food from the meal
  - `total_calories()` — calories of the meal
  - `macros()` — macros of the meal
  - `dominant_macro()` — the macronutrient with the largest energy share
- **Associations:** `FoodPortion` (parameter)

#### `Supplement`

A supplement (creatine, vitamin D…) with a maximum daily dose. File: `fitness/nutrition/supplement.py`.

- **Fields:** `_name`, `_dose_mg`, `_max_daily_mg`, `_taken_today_mg`
- **Methods:**
  - `take(doses)` — takes doses, enforcing the daily limit
  - `remaining_mg()` — how much more can be taken
  - `doses_left()` — how many doses are left
  - `reset_day()` — resets the daily tally

### goals — goals, streaks, achievements, challenges

#### `Achievement`

A badge unlocked when a metric reaches a threshold. File: `fitness/goals/achievement.py`.

- **Fields:** `_code`, `_title`, `_metric`, `_threshold`, `_points`, `_unlocked_at`
- **Methods:**
  - `is_unlocked()` — whether the achievement has been earned
  - `unlock(now)` — awards the achievement (a second time is an error)
  - `try_unlock(metric, value, now)` — awards the achievement if the metric has reached the threshold

#### `AchievementBoard`

A user's set of achievements and point counting. File: `fitness/goals/achievement_board.py`.

- **Fields:** `_user`, `_achievements`
- **Methods:**
  - `add(achievement)` — adds an achievement to the board
  - `evaluate(metric, value, now)` — checks a metric and returns newly earned achievements
  - `unlocked()` — earned achievements
  - `total_points()` — sum of points
  - `completion_percent()` — percentage of achievements earned
- **Associations:** `Achievement` (parameter), `User` (field)

#### `ChallengeEntry`

The result of one challenge participant. File: `fitness/goals/challenge_entry.py`.

- **Fields:** `_user`, `_total`, `_contributions`
- **Methods:**
  - `add(value)` — adds a participant's result
- **Associations:** `User` (field)

#### `Challenge`

A challenge with a metric, a target value and a running period. File: `fitness/goals/challenge.py`.

- **Fields:** `_title`, `_metric`, `_target_value`, `_starts_on`, `_ends_on`, `_max_participants`, `_entries`
- **Methods:**
  - `is_active(today)` — whether the challenge is running on the given day
  - `join(user, today)` — enrols a participant, checking spots and dates
  - `leave(user)` — removes a participant
  - `record(user, value, today)` — credits a result to a participant
  - `leaderboard()` — leaderboard
  - `finishers()` — participants who reached the target
  - `winner(today)` — the winner after the end
- **Associations:** `User` (parameter)

#### `FitnessGoal`

A goal with numeric progress and a deadline. File: `fitness/goals/fitness_goal.py`.

- **Fields:** `_title`, `_start_value`, `_target_value`, `_deadline`, `_current_value`, `_status`
- **Constants:** `ACTIVE`, `ACHIEVED`, `ABANDONED`
- **Methods:**
  - `update_progress(value)` — records the current value and changes the status when reached
  - `progress_percent()` — percentage of goal completion
  - `is_achieved()` — whether the goal is achieved
  - `days_left(today)` — days until the deadline
  - `is_overdue(today)` — whether an active goal is overdue
  - `abandon()` — cancels the goal

#### `WeightGoal` (inherits `FitnessGoal`)

A body-weight goal (loss or gain). File: `fitness/goals/weight_goal.py`.

- **Methods:**
  - `is_weight_loss()` — is it a weight-loss goal?
  - `record_measurement(measurement)` — updates progress from a body measurement
  - `weekly_change_needed(today)` — weight change needed per week
- **Associations:** `BodyMeasurement` (parameter)

#### `DistanceGoal` (inherits `FitnessGoal`)

A cumulative distance goal (km). File: `fitness/goals/distance_goal.py`.

- **Methods:**
  - `record_activity(activity)` — adds the distance of an activity
  - `remaining_km()` — how many km are left
- **Associations:** `Activity` (parameter)

#### `StrengthGoal` (inherits `FitnessGoal`)

A one-rep-max goal in a strength exercise. File: `fitness/goals/strength_goal.py`.

- **Fields:** `_exercise`
- **Methods:**
  - `record_set(exercise, exercise_set)` — updates progress from the 1RM estimate of a set
- **Associations:** `ExerciseSet` (parameter), `StrengthExercise` (field)

#### `StreakTracker`

Counting consecutive days with completed activity. File: `fitness/goals/streak_tracker.py`.

- **Fields:** `_habit`, `_current_streak`, `_longest_streak`, `_last_day`
- **Methods:**
  - `register(day)` — marks a day and recalculates the streak
  - `register_workout(workout)` — counts the day of a completed workout (`Workout`) towards the streak
  - `is_broken(today)` — whether the streak is broken
  - `reset()` — resets the current streak
- **Associations:** `Workout` (parameter)

### gym — memberships, club, group classes

#### `Locker`

A changing-room locker. File: `fitness/gym/locker.py`.

- **Fields:** `_number`, `_occupant`
- **Methods:**
  - `is_free()` — whether the locker is free
  - `assign(user)` — assigns the locker to a visitor
  - `release()` — frees the locker
- **Associations:** `User` (parameter)

#### `Visit`

A club visit from check-in to check-out. File: `fitness/gym/visit.py`.

- **Fields:** `_user`, `_checked_in_at`, `_locker`, `_checked_out_at`
- **Methods:**
  - `is_open()` — is the visitor still in the club?
  - `check_out(now)` — records the exit and frees the locker
  - `duration_minutes(now)` — visit duration
- **Associations:** `Locker` (field), `User` (field)

#### `Gym`

A fitness club with limited capacity and lockers. File: `fitness/gym/gym.py`.

- **Fields:** `_name`, `_address`, `_capacity`, `_lockers`, `_active_visits`, `_history`
- **Methods:**
  - `visitors_inside()` — who is in the club now
  - `is_full()` — whether capacity is reached
  - `occupancy_percent()` — how full the club is
  - `check_in(membership, now)` — admission with a membership, issuing a locker
  - `check_out(user, now)` — leaving the club and writing to the history
  - `visits_count(user)` — number of visits of a user
- **Associations:** `Membership` (parameter)

#### `GroupClass`

A group workout (yoga, cycling, functional training). File: `fitness/gym/group_class.py`.

- **Fields:** `_title`, `_trainer`, `_workout_type`, `_starts_at`, `_duration_minutes`, `_capacity`, `_attendees`, `_waitlist`
- **Methods:**
  - `ends_at()` — class end time
  - `available_spots()` — free spots
  - `is_full()` — is the class full?
  - `book(membership)` — booking with a membership or joining the waitlist
  - `cancel_booking(user)` — cancels a booking and promotes someone from the waitlist
  - `conflicts_with(other)` — whether it overlaps with a class of the same trainer
- **Associations:** `Membership` (parameter), `Trainer` (field)

#### `MembershipPlan`

A membership tariff. File: `fitness/gym/membership_plan.py`.

- **Fields:** `_name`, `_monthly_price`, `_duration_months`, `_includes_group_classes`, `_max_freezes`
- **Methods:**
  - `total_price(discount_percent)` — tariff price with a discount
  - `duration_days()` — validity period in days
  - `price_per_day()` — price of one day

#### `Payment`

A payment: cash (with change) or card (exact amount). File: `fitness/gym/payment.py`.

- **Fields:** `_amount`, `_method`, `_created_at`, `_status`, `_paid_amount`
- **Constants:** `PENDING`, `PAID`, `REFUNDED`, `CASH`, `CARD`
- **Methods:**
  - `pay(given_amount)` — processes the payment and returns change
  - `refund()` — refunds a processed payment
  - `is_paid()` — has the payment been processed?

#### `Membership`

A user's membership: activation, freezing, renewal, cancellation. File: `fitness/gym/membership.py`.

- **Fields:** `_user`, `_plan`, `_start_date`, `_end_date`, `_status`, `_freezes_used`, `_frozen_since`, `_payments`
- **Constants:** `PENDING`, `ACTIVE`, `FROZEN`, `CANCELLED`, `MAX_FREEZE_DAYS`
- **Methods:**
  - `activate(payment)` — activates the membership after full payment
  - `is_valid(on_date)` — whether the membership is valid on a date
  - `require_access(on_date)` — checks access (freeze, expiry)
  - `allows_group_classes()` — whether group classes are included
  - `freeze(on_date)` — freezes the membership within the limit
  - `unfreeze(on_date)` — unfreezes and extends the term by the frozen days
  - `renew(payment)` — renews the membership with a new payment
  - `cancel()` — cancels the membership
  - `days_remaining(on_date)` — days until expiry
- **Associations:** `MembershipPlan` (field), `Payment` (parameter), `User` (field)

### reports — reports, reminders, notifications

#### `Reminder`

A recurring reminder at a given time on given weekdays. File: `fitness/reports/reminder.py`.

- **Fields:** `_message`, `_remind_at`, `_weekdays`, `_active`, `_last_fired_on`
- **Methods:**
  - `activate()` — turns the reminder on
  - `deactivate()` — turns the reminder off
  - `clashes_with(other)` — whether it coincides in time and days with another
  - `is_due(now)` — whether it is time to fire
  - `mark_fired(now)` — records that it fired for the day
  - `next_occurrence(now)` — the next firing time

#### `Notification`

A notification for a user. File: `fitness/reports/notification.py`.

- **Fields:** `_title`, `_body`, `_created_at`, `_read`
- **Methods:**
  - `mark_read()` — marks it as read
  - `age_minutes(now)` — age of the notification in minutes

#### `NotificationCenter`

A user's notifications and reminders, honouring their settings. File: `fitness/reports/notification_center.py`.

- **Fields:** `_user`, `_notifications`, `_reminders`
- **Methods:**
  - `push(notification)` — delivers a notification if they are enabled
  - `add_reminder(reminder)` — adds a reminder without conflicts
  - `process_reminders(now)` — turns due reminders into notifications
  - `unread_count()` — number of unread notifications
  - `mark_all_read()` — marks everything as read
  - `clear_read()` — deletes read notifications
- **Associations:** `Notification` (parameter), `Reminder` (parameter), `User` (field)

#### `ProgressReport`

A summary of a user's completed workouts over a period. File: `fitness/reports/progress_report.py`.

- **Fields:** `_user`, `_period_start`, `_period_end`, `_workouts`
- **Methods:**
  - `workouts_count()` — number of completed workouts in the period
  - `total_volume()` — total tonnage
  - `average_duration()` — average duration
  - `most_trained_muscle()` — the most trained muscle
  - `weeks_in_period()` — number of weeks in the period
  - `consistency_percent()` — regularity relative to the weekly target
  - `summary()` — text summary
- **Associations:** `User` (field), `Workout` (parameter)

## Association summary

An association is a class included in another as a field or as a method parameter.

| # | Class | Linked with | Kind |
|---|---|---|---|
| 1 | `AchievementBoard` | `Achievement` | parameter |
| 2 | `AchievementBoard` | `User` | field |
| 3 | `Activity` | `User` | field |
| 4 | `CalorieCalculator` | `BodyMeasurement` | parameter |
| 5 | `CalorieCalculator` | `User` | parameter |
| 6 | `Challenge` | `User` | parameter |
| 7 | `ChallengeEntry` | `User` | field |
| 8 | `CyclingActivity` | `Route` | field |
| 9 | `DailyActivity` | `SleepRecord` | parameter |
| 10 | `DistanceGoal` | `Activity` | parameter |
| 11 | `Exercise` | `Equipment` | field |
| 12 | `Exercise` | `MuscleGroup` | field |
| 13 | `ExerciseLibrary` | `Exercise` | parameter |
| 14 | `FitnessTracker` | `BodyMeasurement` | parameter |
| 15 | `FitnessTracker` | `CalorieCalculator` | field |
| 16 | `FitnessTracker` | `ExerciseLibrary` | field |
| 17 | `FitnessTracker` | `FitnessGoal` | parameter |
| 18 | `FitnessTracker` | `Meal` | parameter |
| 19 | `FitnessTracker` | `PasswordPolicy` | field |
| 20 | `FitnessTracker` | `StrengthGoal` | parameter |
| 21 | `FitnessTracker` | `WeightGoal` | parameter |
| 22 | `FitnessTracker` | `Workout` | parameter |
| 23 | `FoodPortion` | `Food` | field |
| 24 | `GroupClass` | `Membership` | parameter |
| 25 | `GroupClass` | `Trainer` | field |
| 26 | `Gym` | `Membership` | parameter |
| 27 | `HealthProfile` | `BalanceExercise` | parameter |
| 28 | `HealthProfile` | `Injury` | parameter |
| 29 | `HeartRateMonitor` | `HeartRateSample` | parameter |
| 30 | `HeartRateMonitor` | `HeartRateZone` | field |
| 31 | `Injury` | `FlexibilityExercise` | parameter |
| 32 | `Injury` | `MuscleGroup` | field |
| 33 | `Locker` | `User` | parameter |
| 34 | `Meal` | `FoodPortion` | parameter |
| 35 | `Membership` | `MembershipPlan` | field |
| 36 | `Membership` | `Payment` | parameter |
| 37 | `Membership` | `User` | field |
| 38 | `NotificationCenter` | `Notification` | parameter |
| 39 | `NotificationCenter` | `Reminder` | parameter |
| 40 | `NotificationCenter` | `User` | field |
| 41 | `NutritionDiary` | `MacroTargets` | parameter |
| 42 | `NutritionDiary` | `Meal` | parameter |
| 43 | `NutritionDiary` | `Supplement` | parameter |
| 44 | `NutritionDiary` | `User` | field |
| 45 | `ProgressReport` | `User` | field |
| 46 | `ProgressReport` | `Workout` | parameter |
| 47 | `RestTimer` | `StrengthExercise` | parameter |
| 48 | `Route` | `CardioExercise` | parameter |
| 49 | `Route` | `GpsPoint` | parameter |
| 50 | `RunActivity` | `Route` | field |
| 51 | `StreakTracker` | `Workout` | parameter |
| 52 | `StrengthGoal` | `ExerciseSet` | parameter |
| 53 | `StrengthGoal` | `StrengthExercise` | field |
| 54 | `TemplateItem` | `Exercise` | field |
| 55 | `Trainer` | `Certification` | parameter |
| 56 | `Trainer` | `User` | parameter |
| 57 | `TrainingSession` | `Trainer` | field |
| 58 | `TrainingSession` | `User` | field |
| 59 | `User` | `BodyMeasurement` | parameter |
| 60 | `User` | `HealthProfile` | field |
| 61 | `User` | `PasswordPolicy` | parameter |
| 62 | `User` | `UserSettings` | field |
| 63 | `Visit` | `Locker` | field |
| 64 | `Visit` | `User` | field |
| 65 | `WearableDevice` | `DailyActivity` | parameter |
| 66 | `WearableDevice` | `HeartRateMonitor` | parameter |
| 67 | `WearableDevice` | `SwimmingActivity` | parameter |
| 68 | `WearableDevice` | `User` | parameter |
| 69 | `WeightGoal` | `BodyMeasurement` | parameter |
| 70 | `Workout` | `User` | field |
| 71 | `Workout` | `WorkoutEntry` | parameter |
| 72 | `WorkoutEntry` | `Exercise` | field |
| 73 | `WorkoutEntry` | `ExerciseSet` | parameter |
| 74 | `WorkoutEntry` | `StrengthExercise` | parameter |
| 75 | `WorkoutPlan` | `WorkoutTemplate` | parameter |
| 76 | `WorkoutTemplate` | `TemplateItem` | parameter |
| 77 | `WorkoutTemplate` | `User` | parameter |

## Testing

The tests live in `tests/` (one file per package, plus `test_application.py` and `test_cli.py`) and cover both the main scenarios and the error branches (exceptions, boundary values). The 90 % coverage threshold is set in `pyproject.toml` (`--cov-fail-under=90`), so `pytest` fails if coverage drops below it.
