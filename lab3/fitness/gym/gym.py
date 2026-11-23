from fitness.exceptions import CapacityExceededError, DuplicateEntityError, EntityNotFoundError
from fitness.gym.locker import Locker
from fitness.gym.membership import Membership
from fitness.gym.visit import Visit
from fitness.validation import ensure_count, ensure_instance, ensure_text


class Gym:
    """Фитнес-клуб с ограниченной вместимостью и шкафчиками."""

    def __init__(self, name, address, capacity, locker_count):
        self._name = ensure_text(name, "название клуба")
        self._address = ensure_text(address, "адрес")
        self._capacity = ensure_count(capacity, "вместимость", minimum=1)
        self._lockers = [Locker(number) for number in range(1, ensure_count(locker_count, "шкафчики") + 1)]
        self._active_visits = {}
        self._history = []

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def capacity(self):
        return self._capacity

    @property
    def lockers(self):
        return tuple(self._lockers)

    @property
    def history(self):
        return tuple(self._history)

    def visitors_inside(self):
        return [visit.user for visit in self._active_visits.values()]

    def is_full(self):
        return len(self._active_visits) >= self._capacity

    def occupancy_percent(self):
        return round(len(self._active_visits) / self._capacity * 100, 1)

    def _free_locker(self):
        return next((locker for locker in self._lockers if locker.is_free()), None)

    def check_in(self, membership, now):
        ensure_instance(membership, Membership, "абонемент")
        membership.require_access(now.date())
        user = membership.user
        if user.username in self._active_visits:
            raise DuplicateEntityError(f"{user.username} уже в клубе")
        if self.is_full():
            raise CapacityExceededError(f"Клуб «{self._name}» заполнен")
        locker = self._free_locker()
        if locker is not None:
            locker.assign(user)
        visit = Visit(user, now, locker)
        self._active_visits[user.username] = visit
        return visit

    def check_out(self, user, now):
        visit = self._active_visits.pop(getattr(user, "username", None), None)
        if visit is None:
            raise EntityNotFoundError("Посетитель не находится в клубе")
        visit.check_out(now)
        self._history.append(visit)
        return visit

    def visits_count(self, user):
        return sum(1 for visit in self._history if visit.user is user)
