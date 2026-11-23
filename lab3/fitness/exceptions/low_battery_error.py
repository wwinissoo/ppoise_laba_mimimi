from fitness.exceptions.device_error import DeviceError


class LowBatteryError(DeviceError):
    """Заряда батареи недостаточно для операции."""
