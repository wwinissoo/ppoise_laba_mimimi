from fitness.exceptions.membership_error import MembershipError


class MembershipFrozenError(MembershipError):
    """Абонемент заморожен либо лимит заморозок исчерпан."""
