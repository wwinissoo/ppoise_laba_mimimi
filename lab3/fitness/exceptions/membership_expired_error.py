from fitness.exceptions.membership_error import MembershipError


class MembershipExpiredError(MembershipError):
    """Абонемент неактивен или истёк."""
