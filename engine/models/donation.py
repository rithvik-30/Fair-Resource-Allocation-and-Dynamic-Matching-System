from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from engine.models.location import Location


class Donation(BaseModel):
    """Represents a batch of surplus food offered by a donor."""
    id: str = Field(..., description="Unique donation ID")
    donor_id: str = Field(..., description="Reference ID of the donor")
    food_type: str = Field(..., description="Category of food item")
    quantity: float = Field(
        ..., gt=0.0, description="Offered food quantity in kg"
    )
    perishable: bool = Field(
        default=False, description="Flag indicating perishable food"
    )
    expiration_hours: Optional[float] = Field(
        default=None, gt=0.0, description="Expiration time window in hours"
    )
    requires_refrigeration: bool = Field(
        default=False, description="Whether cold chain transport is required"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Donation creation timestamp",
    )
    location: Optional[Location] = Field(
        default=None,
        description="Pickup location coordinates (defaults to Donor location if None)",
    )
