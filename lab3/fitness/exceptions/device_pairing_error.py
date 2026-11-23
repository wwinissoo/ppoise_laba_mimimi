from fitness.exceptions.device_error import DeviceError


class DevicePairingError(DeviceError):
    """Устройство не сопряжено или уже сопряжено с другим пользователем."""
