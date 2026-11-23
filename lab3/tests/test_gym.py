from datetime import timedelta

import pytest

from fitness.exceptions import (
    CapacityExceededError,
    DuplicateEntityError,
    EntityNotFoundError,
    InvalidValueError,
    MembershipError,
    MembershipExpiredError,
    MembershipFrozenError,
    PaymentDeclinedError,
    ScheduleConflictError,
)
from fitness.gym import GroupClass, Gym, Locker, Membership, MembershipPlan, Payment, Visit
from fitness.users import Trainer
from tests.conftest import NOW, TODAY


def paid(amount, method=Payment.CARD):
    payment = Payment(amount, method, NOW)
    payment.pay(amount)
    return payment


@pytest.fixture
def plan():
    return MembershipPlan("Стандарт", 3000, 3, True, 1)


def active_membership(user, plan):
    membership = Membership(user, plan, TODAY)
    membership.activate(paid(plan.total_price()))
    return membership


class TestMembershipPlanAndPayment:
    def test_plan(self, plan):
        assert plan.total_price() == 9000 and plan.total_price(10) == 8100
        assert plan.duration_days() == 90 and plan.price_per_day() == 100
        assert (plan.name, plan.monthly_price, plan.duration_months, plan.includes_group_classes, plan.max_freezes) == (
            "Стандарт",
            3000,
            3,
            True,
            1,
        )

    def test_payment(self):
        card = Payment(9000, Payment.CARD, NOW)
        with pytest.raises(PaymentDeclinedError):
            card.pay(8000)
        with pytest.raises(PaymentDeclinedError):
            card.pay(9500)
        assert card.pay(9000) == 0 and card.is_paid() and card.paid_amount == 9000
        with pytest.raises(PaymentDeclinedError):
            card.pay(9000)
        assert card.refund() == 9000 and card.status == Payment.REFUNDED and card.paid_amount == 0
        with pytest.raises(PaymentDeclinedError):
            card.refund()
        cash = Payment(900, Payment.CASH, NOW)
        assert cash.pay(1000) == 100 and cash.method == Payment.CASH and cash.amount == 900 and cash.created_at == NOW


class TestMembership:
    def test_lifecycle(self, user, plan):
        membership = Membership(user, plan, TODAY)
        with pytest.raises(MembershipExpiredError):
            membership.require_access(TODAY)
        with pytest.raises(PaymentDeclinedError):
            membership.activate(Payment(9000, Payment.CARD, NOW))
        with pytest.raises(PaymentDeclinedError):
            membership.activate(paid(100))
        membership.activate(paid(9000))
        with pytest.raises(MembershipError):
            membership.activate(paid(9000))
        assert membership.is_valid(TODAY) and membership.end_date == TODAY + timedelta(days=90)
        assert membership.allows_group_classes() and membership.days_remaining(TODAY) == 90
        membership.freeze(TODAY)
        with pytest.raises(MembershipFrozenError):
            membership.require_access(TODAY)
        assert membership.unfreeze(TODAY + timedelta(days=10)) == 10 and membership.days_remaining(TODAY) == 100
        with pytest.raises(MembershipError):
            membership.unfreeze(TODAY)
        with pytest.raises(MembershipFrozenError):
            membership.freeze(TODAY)
        assert membership.renew(paid(9000)) == TODAY + timedelta(days=190) and len(membership.payments) == 2
        assert membership.freezes_used == 1 and membership.user is user and membership.plan is plan
        assert membership.start_date == TODAY and membership.status == Membership.ACTIVE
        membership.cancel()
        with pytest.raises(MembershipError):
            membership.cancel()
        with pytest.raises(MembershipError):
            membership.renew(paid(9000))
        assert membership.days_remaining(TODAY + timedelta(days=500)) == 0


class TestFacility:
    def test_locker_and_visit(self, user):
        locker = Locker(7)
        with pytest.raises(InvalidValueError):
            locker.release()
        locker.assign(user)
        with pytest.raises(CapacityExceededError):
            locker.assign(user)
        visit = Visit(user, NOW, locker)
        assert visit.duration_minutes(NOW + timedelta(minutes=15)) == 15 and visit.is_open()
        with pytest.raises(InvalidValueError):
            visit.check_out(NOW - timedelta(minutes=1))
        visit.check_out(NOW + timedelta(minutes=30))
        assert locker.is_free() and visit.duration_minutes() == 30 and not visit.is_open()
        with pytest.raises(InvalidValueError):
            visit.check_out(NOW + timedelta(hours=1))
        assert visit.user is user and visit.locker is locker and visit.checked_in_at == NOW and visit.checked_out_at
        assert locker.number == 7 and locker.occupant is None and Visit(user, NOW).duration_minutes() == 0
        free_visit = Visit(user, NOW)
        free_visit.check_out(NOW + timedelta(minutes=5))
        assert free_visit.duration_minutes() == 5

    def test_gym(self, user, other_user, plan):
        gym = Gym("Атлет", "ул. Ленина, 1", 1, 1)
        first, second = active_membership(user, plan), active_membership(other_user, plan)
        visit = gym.check_in(first, NOW)
        assert visit.locker.number == 1 and gym.is_full() and gym.occupancy_percent() == 100
        assert gym.visitors_inside() == [user]
        with pytest.raises(DuplicateEntityError):
            gym.check_in(first, NOW)
        with pytest.raises(CapacityExceededError):
            gym.check_in(second, NOW)
        assert gym.check_out(user, NOW + timedelta(minutes=90)).duration_minutes() == 90
        with pytest.raises(EntityNotFoundError):
            gym.check_out(user, NOW)
        assert gym.visits_count(user) == 1 and gym.visits_count(other_user) == 0 and len(gym.history) == 1
        assert (gym.name, gym.address, gym.capacity, len(gym.lockers)) == ("Атлет", "ул. Ленина, 1", 1, 1)
        no_lockers = Gym("Мини", "ул. Мира, 2", 2, 0)
        assert no_lockers.check_in(second, NOW).locker is None


class TestGroupClass:
    def test_booking(self, user, other_user, plan):
        trainer = Trainer("Ира", ["йога"], 1000)
        with pytest.raises(ScheduleConflictError):
            GroupClass("Бокс", trainer, "бокс", NOW, 60, 1)
        yoga = GroupClass("Утренняя йога", trainer, "йога", NOW, 60, 1)
        first, second = active_membership(user, plan), active_membership(other_user, plan)
        assert yoga.book(first) and not yoga.book(second) and yoga.waitlist == (other_user,)
        with pytest.raises(DuplicateEntityError):
            yoga.book(first)
        assert yoga.is_full() and yoga.available_spots() == 0
        assert yoga.cancel_booking(user) is other_user and yoga.attendees == (other_user,)
        assert yoga.book(first) is False and yoga.cancel_booking(user) is None
        assert yoga.cancel_booking(other_user) is None
        with pytest.raises(EntityNotFoundError):
            yoga.cancel_booking(other_user)
        basic = Membership(user, MembershipPlan("Базовый", 2000, 1), TODAY)
        basic.activate(paid(2000))
        with pytest.raises(MembershipError):
            yoga.book(basic)
        later = GroupClass("Вечерняя", trainer, "йога", NOW + timedelta(minutes=30), 60, 5)
        other_trainer = GroupClass("Другая", Trainer("Оля", ["йога"], 900), "йога", NOW, 60, 5)
        assert yoga.conflicts_with(later) and not yoga.conflicts_with(other_trainer)
        assert yoga.ends_at() == NOW + timedelta(hours=1) and yoga.title and yoga.trainer is trainer
        assert (yoga.workout_type, yoga.starts_at, yoga.duration_minutes, yoga.capacity) == ("йога", NOW, 60, 1)
