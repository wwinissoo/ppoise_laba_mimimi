from datetime import date

import pytest

from fitness.exceptions import (
    CapacityExceededError,
    DuplicateEntityError,
    EntityNotFoundError,
    InjuryRiskError,
    InvalidCredentialsError,
    InvalidMeasurementError,
    InvalidValueError,
    WeakPasswordError,
)
from fitness.users import (
    BodyMeasurement,
    Certification,
    HealthProfile,
    Injury,
    PasswordPolicy,
    Trainer,
    User,
    UserSettings,
)
from tests.conftest import PASSWORD, TODAY


class TestPasswordPolicy:
    def test_violations_and_validate(self, policy):
        assert policy.find_violations("Secret123") == []
        assert len(policy.find_violations("abc")) == 3
        assert policy.find_violations(123) == ["пароль должен быть строкой"]
        with pytest.raises(WeakPasswordError):
            policy.validate("short")
        strict = PasswordPolicy(4, False, False, True)
        assert strict.find_violations("abcd") == ["спецсимвол"] and strict.validate("ab!d") == "ab!d"
        assert (strict.min_length, strict.require_digit, strict.require_uppercase, strict.require_special) == (
            4,
            False,
            False,
            True,
        )

    def test_strength_and_hash(self, policy):
        assert policy.strength_score("") == 0 and policy.strength_score(None) == 0
        assert policy.strength_score("Secret123!Secret123") == 5
        salt = policy.generate_salt()
        hashed = policy.hash_password("pw", salt)
        assert policy.matches("pw", salt, hashed) and not policy.matches("bad", salt, hashed)
        assert not policy.matches(None, salt, hashed)

    def test_invalid_length(self):
        with pytest.raises(InvalidValueError):
            PasswordPolicy(0)


class TestBodyMeasurement:
    def test_metrics(self, measurement):
        assert measurement.bmi() == 20.8 and measurement.bmi_category() == "норма"
        assert measurement.lean_mass_kg() == 46.8 and measurement.waist_to_height_ratio() == 0.41
        assert (measurement.measured_on, measurement.weight_kg, measurement.height_cm) == (TODAY, 60, 170)
        assert measurement.body_fat_percent == 22 and measurement.waist_cm == 70

    @pytest.mark.parametrize("weight, label", [(50, "дефицит массы"), (80, "избыточный вес"), (100, "ожирение")])
    def test_categories(self, weight, label):
        assert BodyMeasurement(TODAY, weight, 170).bmi_category() == label

    def test_missing_and_invalid(self, measurement):
        bare = BodyMeasurement(date(2026, 1, 1), 62, 170)
        with pytest.raises(InvalidMeasurementError):
            bare.lean_mass_kg()
        with pytest.raises(InvalidMeasurementError):
            bare.waist_to_height_ratio()
        assert measurement.weight_difference(bare) == -2
        with pytest.raises(InvalidMeasurementError):
            BodyMeasurement(TODAY, 5, 170)
        with pytest.raises(TypeError):
            measurement.weight_difference("62")


class TestInjury:
    def test_lifecycle(self, chest, legs):
        injury = Injury(chest, Injury.MODERATE, date(2026, 11, 1), " растяжение ")
        assert injury.is_active() and injury.affects(chest) and not injury.affects(legs)
        assert injury.expected_recovery_date() == date(2026, 11, 22) and injury.description == "растяжение"
        assert (injury.muscle_group, injury.severity, injury.occurred_on) == (chest, "средняя", date(2026, 11, 1))
        with pytest.raises(InvalidValueError):
            injury.mark_recovered(date(2026, 10, 1))
        injury.mark_recovered(TODAY)
        assert not injury.is_active() and injury.recovered_on == TODAY and not injury.affects(chest)

    def test_validation(self, chest):
        with pytest.raises(InvalidValueError):
            Injury(chest, "смертельная", TODAY)
        with pytest.raises(TypeError):
            Injury("грудь", Injury.MILD, TODAY)
        assert Injury(chest, Injury.MILD, TODAY, None).description == ""


class TestHealthProfile:
    def test_pressure_and_heart(self):
        profile = HealthProfile(60)
        assert not profile.is_hypertensive() and profile.max_heart_rate(30) == 187
        assert profile.heart_rate_reserve(30) == 127
        profile.update_pressure(150, 95)
        assert profile.is_hypertensive() and profile.systolic_pressure == 150 and profile.diastolic_pressure == 95
        with pytest.raises(InvalidMeasurementError):
            profile.update_pressure(80, 90)
        with pytest.raises(InvalidMeasurementError):
            HealthProfile(10)

    def test_injuries_and_conditions(self, chest, bench_press, running):
        profile = HealthProfile(65)
        profile.add_condition("Астма")
        profile.add_condition("астма")
        assert profile.chronic_conditions == ("Астма",) and profile.resting_heart_rate == 65
        injury = Injury(chest, Injury.SEVERE, TODAY)
        profile.add_injury(injury)
        assert profile.injuries == (injury,) and profile.active_injuries() == [injury]
        assert profile.check_exercise_allowed(running)
        with pytest.raises(InjuryRiskError):
            profile.check_exercise_allowed(bench_press)


class TestUserSettings:
    def test_behaviour(self):
        settings = UserSettings()
        assert settings.format_weight(10) == "10.0 кг" and settings.language == "ru"
        assert settings.switch_unit_system() == UserSettings.IMPERIAL and settings.format_weight(10) == "22.0 lb"
        assert settings.switch_unit_system() == UserSettings.METRIC
        assert settings.toggle_notifications() is False and not settings.notifications_enabled
        settings.set_weekly_target(5)
        assert settings.weekly_workout_target == 5 and settings.unit_system == UserSettings.METRIC
        with pytest.raises(InvalidValueError):
            settings.set_weekly_target(20)


class TestUser:
    def test_registration_and_password(self, user, policy):
        assert user.email == "anna@example.com" and user.verify_password(PASSWORD)
        assert user.username == "anna" and user.gender == User.FEMALE and user.birth_date == date(2000, 5, 20)
        assert isinstance(user.health_profile, HealthProfile) and isinstance(user.settings, UserSettings)
        with pytest.raises(InvalidCredentialsError):
            user.change_password("wrong", "NewPass123", policy)
        with pytest.raises(InvalidValueError):
            user.change_password(PASSWORD, PASSWORD, policy)
        user.change_password(PASSWORD, "NewPass123", policy)
        assert user.verify_password("NewPass123") and not user.verify_password(PASSWORD)
        with pytest.raises(WeakPasswordError):
            User.register("x", "x@x.ru", "weak", date(2000, 1, 1), User.MALE, policy)

    def test_age_and_email(self, user):
        assert user.age(date(2026, 5, 19)) == 25 and user.age(date(2026, 5, 20)) == 26 and user.age() > 0
        user.update_email("NEW@mail.ru")
        assert user.email == "new@mail.ru"
        for bad in ("no-at", "@mail.ru", "a@mail", "a@.ru", "a@ru."):
            with pytest.raises(InvalidValueError):
                user.update_email(bad)

    def test_measurements(self, user, measurement):
        assert user.latest_measurement() is None and user.weight_change() == 0
        user.add_measurement(measurement)
        user.add_measurement(BodyMeasurement(date(2026, 10, 1), 63, 170))
        assert user.latest_measurement() is measurement and user.weight_change() == -3
        assert len(user.measurements) == 2
        with pytest.raises(DuplicateEntityError):
            user.add_measurement(BodyMeasurement(TODAY, 61, 170))


class TestCertificationAndTrainer:
    def test_certification(self):
        cert = Certification("Фитнес-инструктор", "ФПФР", date(2026, 12, 1))
        assert cert.is_valid(TODAY) and cert.days_until_expiry(TODAY) == 15
        assert cert.days_until_expiry(date(2027, 1, 1)) == 0 and cert.title and cert.issuer
        assert cert.valid_until == date(2026, 12, 1)

    def test_trainer(self, user, other_user):
        trainer = Trainer("Пётр Иванов", ["Йога", "Силовая"], 1200, max_clients=1)
        assert trainer.specializations == ("йога", "силовая")
        assert trainer.can_lead("СИЛОВАЯ") and not trainer.can_lead(5) and not trainer.is_certified(TODAY)
        trainer.add_certification(Certification("Йога", "YA", date(2027, 1, 1)))
        assert trainer.is_certified(TODAY) and len(trainer.certifications) == 1
        trainer.assign_client(user)
        with pytest.raises(DuplicateEntityError):
            trainer.assign_client(user)
        with pytest.raises(CapacityExceededError):
            trainer.assign_client(other_user)
        assert trainer.clients == (user,) and trainer.session_fee(90) == 1800
        trainer.release_client(user)
        with pytest.raises(EntityNotFoundError):
            trainer.release_client(user)
        assert trainer.full_name == "Пётр Иванов" and trainer.hourly_rate == 1200 and trainer.max_clients == 1
