from enum import Enum


class RequestStatus(str, Enum):
    """Lifecycle status of a rescue request transport task."""
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_TRANSIT = "IN_TRANSIT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class MatchStatus(str, Enum):
    """Lifecycle status of a volunteer match assignment."""
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
