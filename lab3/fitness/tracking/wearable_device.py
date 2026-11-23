from datetime import datetime

from fitness.exceptions import DevicePairingError, LowBatteryError
from fitness.tracking.daily_activity import DailyActivity
from fitness.tracking.heart_rate_monitor import HeartRateMonitor
from fitness.tracking.heart_rate_sample import HeartRateSample
from fitness.tracking.swimming_activity import SwimmingActivity
from fitness.users.user import User
from fitness.validation import ensure_count, ensure_instance, ensure_number, ensure_text


class WearableDevice:
    """Фитнес-браслет: сопряжение, синхронизация, заряд и прошивка."""

    FULL_BATTERY = 100
    SYNC_MIN_BATTERY = 5
    FIRMWARE_MIN_BATTERY = 30
    SYNC_DRAIN = 2
    MEASUREMENT_DRAIN = 1

    def __init__(self, model, serial_number, firmware_version="1.0.0", battery_percent=FULL_BATTERY):
        self._model = ensure_text(model, "модель")
        self._serial_number = ensure_text(serial_number, "серийный номер")
        self._firmware_version = self._parse_version(firmware_version)
        self._battery_percent = ensure_number(battery_percent, "заряд", 0, self.FULL_BATTERY)
        self._paired_user = None
        self._last_synced_at = None

    @staticmethod
    def _parse_version(version):
        text = ensure_text(version, "версия прошивки")
        parts = text.split(".")
        if not all(part.isdigit() for part in parts):
            raise DevicePairingError(f"Некорректная версия прошивки «{text}»")
        return tuple(int(part) for part in parts)

    @property
    def model(self):
        return self._model

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def firmware_version(self):
        return ".".join(str(part) for part in self._firmware_version)

    @property
    def battery_percent(self):
        return self._battery_percent

    @property
    def paired_user(self):
        return self._paired_user

    @property
    def last_synced_at(self):
        return self._last_synced_at

    def pair(self, user):
        ensure_instance(user, User, "пользователь")
        if self._paired_user is not None and self._paired_user is not user:
            raise DevicePairingError(f"Устройство уже сопряжено с {self._paired_user.username}")
        self._paired_user = user

    def unpair(self):
        if self._paired_user is None:
            raise DevicePairingError("Устройство не сопряжено")
        self._paired_user = None

    def _consume_battery(self, minimum, drain):
        if self._battery_percent < minimum:
            raise LowBatteryError(f"Заряд {self._battery_percent}% — нужно не меньше {minimum}%")
        self._battery_percent = max(0, self._battery_percent - drain)

    def _require_paired(self):
        if self._paired_user is None:
            raise DevicePairingError("Сначала сопрягите устройство с пользователем")

    def sync_steps(self, daily_activity, steps, now):
        """Передаёт накопленные шаги в дневную статистику."""
        self._require_paired()
        ensure_instance(daily_activity, DailyActivity, "дневная активность")
        ensure_instance(now, datetime, "время синхронизации")
        self._consume_battery(self.SYNC_MIN_BATTERY, self.SYNC_DRAIN)
        self._last_synced_at = now
        return daily_activity.add_steps(steps)

    def measure_heart_rate(self, monitor, bpm, now):
        self._require_paired()
        ensure_instance(monitor, HeartRateMonitor, "пульсомер")
        self._consume_battery(self.MEASUREMENT_DRAIN, self.MEASUREMENT_DRAIN)
        sample = HeartRateSample(bpm, now)
        monitor.record(sample)
        return sample

    def charge(self, percent):
        ensure_count(percent, "процент зарядки", minimum=1)
        self._battery_percent = min(self.FULL_BATTERY, self._battery_percent + percent)
        return self._battery_percent

    def update_firmware(self, version):
        new_version = self._parse_version(version)
        if new_version <= self._firmware_version:
            raise DevicePairingError("Новая прошивка должна быть новее текущей")
        self._consume_battery(self.FIRMWARE_MIN_BATTERY, self.SYNC_DRAIN)
        self._firmware_version = new_version

    def needs_sync(self, now, max_hours=24):
        if self._last_synced_at is None:
            return True
        return (now - self._last_synced_at).total_seconds() > max_hours * 3600

    def import_swim(self, activity, now):
        ensure_instance(activity, SwimmingActivity, "заплыв")
        self._require_paired()
        if activity.user is not self._paired_user:
            raise DevicePairingError("Заплыв записан другим пользователем")
        self._consume_battery(self.SYNC_MIN_BATTERY, self.SYNC_DRAIN)
        self._last_synced_at = ensure_instance(now, datetime, "время синхронизации")
        return activity.distance_meters()
