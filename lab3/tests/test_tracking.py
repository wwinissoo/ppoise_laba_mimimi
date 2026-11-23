from datetime import date, datetime, timedelta

import pytest

from fitness.exceptions import DevicePairingError, InvalidMeasurementError, InvalidValueError, LowBatteryError
from fitness.tracking import (
    Activity,
    CyclingActivity,
    DailyActivity,
    GpsPoint,
    HeartRateMonitor,
    HeartRateSample,
    HeartRateZone,
    Route,
    RunActivity,
    SleepRecord,
    SwimmingActivity,
    WearableDevice,
)
from tests.conftest import NOW


def make_route(name="Парк", loop=False):
    route = Route(name)
    route.add_point(GpsPoint(53.9, 27.56, NOW, 200))
    route.add_point(GpsPoint(53.909, 27.56, NOW + timedelta(minutes=5), 210))
    route.add_point(GpsPoint(53.9 if loop else 53.918, 27.56, NOW + timedelta(minutes=10), 205))
    return route


class TestGps:
    def test_point(self):
        point = GpsPoint(0, 0, NOW)
        other = GpsPoint(0, 1, NOW + timedelta(seconds=30), 5)
        assert round(point.distance_to(other), 1) == 111.2 and point.seconds_to(other) == 30
        assert (other.latitude, other.longitude, other.altitude_m) == (0, 1, 5) and other.recorded_at
        with pytest.raises(InvalidMeasurementError):
            GpsPoint(95, 0, NOW)

    def test_route(self):
        route = make_route()
        assert route.total_distance_km() == 2.002 and route.elevation_gain_m() == 10
        assert route.duration_seconds() == 600 and not route.is_loop() and len(route.points) == 3
        assert make_route(loop=True).is_loop() and Route("Пусто").duration_seconds() == 0 and route.name == "Парк"
        with pytest.raises(InvalidMeasurementError):
            route.add_point(GpsPoint(0, 0, NOW))


class TestActivities:
    def test_base_activity(self, user):
        activity = Activity(user, NOW, 30)
        later = Activity(user, NOW + timedelta(minutes=20), 30)
        assert activity.overlaps(later) and not activity.overlaps(Activity(user, NOW + timedelta(hours=1), 10))
        assert activity.calories_burned(60) == 157.5 and activity.distance_km() == 0
        assert activity.summary() == "активность: 30 мин, 0.00 км" and activity.user is user
        assert activity.ends_at() == NOW + timedelta(minutes=30) and activity.started_at == NOW
        assert activity.duration_minutes == 30

    def test_run(self, user):
        run = RunActivity(user, NOW, 10, make_route())
        assert run.average_pace() == 5.0 and run.predict_race_minutes(5) == 26.4 and run.route.name == "Парк"
        empty = RunActivity(user, NOW, 10, Route("Пусто"))
        with pytest.raises(InvalidValueError):
            empty.average_pace()
        with pytest.raises(InvalidValueError):
            empty.predict_race_minutes(5)

    def test_cycling(self, user):
        ride = CyclingActivity(user, NOW, 10, make_route(), "горный")
        assert ride.average_speed_kmh() == 12.0 and ride.climbing_rate() == 5.0 and ride.bike_type == "горный"
        assert CyclingActivity(user, NOW, 10, Route("Пусто")).climbing_rate() == 0 and ride.route
        with pytest.raises(InvalidValueError):
            CyclingActivity(user, NOW, 10, make_route(), "трёхколёсный")

    def test_swimming(self, user):
        swim = SwimmingActivity(user, NOW, 20, 25, 40, "брасс")
        assert swim.distance_meters() == 1000 and swim.distance_km() == 1 and swim.pace_per_100m() == 2
        assert swim.swolf(15) == 45 and (swim.pool_length_m, swim.laps, swim.stroke) == (25, 40, "брасс")


class TestHeart:
    def test_sample_and_zone(self):
        sample = HeartRateSample(100, NOW)
        assert sample.is_elevated(60) and not sample.is_elevated(90) and sample.bpm == 100 and sample.recorded_at
        with pytest.raises(InvalidMeasurementError):
            HeartRateSample(300, NOW)
        zone = HeartRateZone("Аэробная", 70, 80)
        assert zone.bounds(200) == (140, 160) and zone.contains(150, 200) and not zone.contains(160, 200)
        assert (zone.name, zone.lower_percent, zone.upper_percent) == ("Аэробная", 70, 80)
        with pytest.raises(InvalidValueError):
            HeartRateZone("X", 80, 70)

    def test_monitor(self):
        monitor = HeartRateMonitor(200)
        assert monitor.average_bpm() == 0 and monitor.peak_bpm() == 0 and len(monitor.zones) == 5
        for minute, bpm in enumerate((150, 150, 190)):
            monitor.record(HeartRateSample(bpm, NOW + timedelta(minutes=minute)))
        aerobic = monitor.zone_of(150)
        assert aerobic.name == "Аэробная" and monitor.zone_of(50) is None and monitor.average_bpm() == 163
        assert (
            monitor.seconds_in_zone(monitor.zone_of(190)) == 0
            and monitor.seconds_in_zone(aerobic) == 120
            and monitor.peak_bpm() == 190
            and not monitor.exceeds_safe_limit()
        )
        assert len(monitor.samples) == 3 and monitor.max_heart_rate == 200
        with pytest.raises(InvalidMeasurementError):
            monitor.record(HeartRateSample(100, NOW))
        custom = HeartRateMonitor(150, [HeartRateZone("Вся", 0, 100)])
        custom.record(HeartRateSample(170, NOW))
        assert custom.exceeds_safe_limit()


class TestDaily:
    def test_daily_activity(self):
        day = DailyActivity(date(2026, 11, 16), 8000)
        assert day.add_steps(4000) == 4000 and day.goal_progress() == 50 and not day.is_goal_reached()
        day.add_steps(6000)
        assert day.goal_progress() == 100 and day.is_goal_reached() and day.distance_km() == 7.5
        assert day.add_active_minutes(30) == 30 and day.climb_floors(5) == 5 and day.floors == 5
        assert (
            day.day == date(2026, 11, 16) and day.step_goal == 8000 and day.steps == 10000 and day.active_minutes == 30
        )

    def test_sleep(self):
        bed = datetime(2026, 11, 15, 23)
        sleep = SleepRecord(bed, bed + timedelta(hours=8), 120, 100, 1)
        assert (
            sleep.duration_hours() == 8 and sleep.restorative_percent() == 45.8 and sleep.quality_label() == "отличный"
        )
        assert (
            sleep.is_sufficient() and sleep.awakenings == 1 and sleep.deep_minutes == 120 and sleep.rem_minutes == 100
        )
        assert SleepRecord(bed, bed + timedelta(hours=8), 100, 60, 4).quality_label() == "нормальный"
        short = SleepRecord(bed, bed + timedelta(hours=5), 30, 30)
        assert short.quality_label() == "плохой" and not short.is_sufficient() and short.went_to_bed == bed
        assert short.woke_up == bed + timedelta(hours=5)
        with pytest.raises(InvalidMeasurementError):
            SleepRecord(bed, bed, 0, 0)
        with pytest.raises(InvalidMeasurementError):
            SleepRecord(bed, bed + timedelta(hours=1), 50, 50)


class TestWearableDevice:
    def test_pairing_and_sync(self, user, other_user):
        device = WearableDevice("Band 8", "SN1", "1.2.0", 10)
        day = DailyActivity(NOW.date())
        assert device.needs_sync(NOW) and device.firmware_version == "1.2.0"
        with pytest.raises(DevicePairingError):
            device.sync_steps(day, 100, NOW)
        with pytest.raises(DevicePairingError):
            device.unpair()
        device.pair(user)
        device.pair(user)
        with pytest.raises(DevicePairingError):
            device.pair(other_user)
        assert device.sync_steps(day, 500, NOW) == 500 and device.battery_percent == 8 and device.last_synced_at == NOW
        assert not device.needs_sync(NOW + timedelta(hours=1)) and device.needs_sync(NOW + timedelta(days=2))
        monitor = HeartRateMonitor(190)
        assert device.measure_heart_rate(monitor, 80, NOW).bpm == 80 and monitor.samples
        with pytest.raises(LowBatteryError):
            device.update_firmware("2.0")
        assert device.charge(200) == 100
        with pytest.raises(DevicePairingError):
            device.update_firmware("1.1.9")
        device.update_firmware("1.10")
        assert device.firmware_version == "1.10" and device.paired_user is user
        assert device.model == "Band 8" and device.serial_number == "SN1"
        device.unpair()
        assert device.paired_user is None
        with pytest.raises(DevicePairingError):
            WearableDevice("X", "Y", "v1")
