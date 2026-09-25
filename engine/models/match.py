from datetime import datetime, timezone
from pydantic import BaseModel, Field
from engine.models.enums import MatchStatus


class Match(BaseModel):
    """Represents an assignment of a RescueRequest to a Volunteer."""
    id: str = Field(..., description="Unique match assignment ID")
    request_id: str = Field(..., description="Target RescueRequest ID")
    volunteer_id: str = Field(..., description="Assigned Volunteer ID")
    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Assignment timestamp",
    )
    estimated_distance: float = Field(
        default=0.0, ge=0.0, description="Estimated total trip distance in km"
    )
    status: MatchStatus = Field(
        default=MatchStatus.ASSIGNED, description="Match state"
    )
