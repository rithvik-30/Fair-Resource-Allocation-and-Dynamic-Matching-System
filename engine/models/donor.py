from typing import Optional, Tuple
from pydantic import BaseModel, Field
from engine.models.location import Location


class Donor(BaseModel):
    """Represents a surplus food provider (supermarket, restaurant, farm)."""
    id: str = Field(..., description="Unique donor ID")
    name: str = Field(..., description="Donor organization name")
    location: Location = Field(..., description="Physical location coordinates")
    operating_hours: Tuple[str, str] = Field(
        default=("08:00", "20:00"),
        description="Operating hours tuple (start_time, end_time) in HH:MM",
    )
    contact_info: Optional[str] = Field(
        default=None, description="Contact information or phone number"
    )
