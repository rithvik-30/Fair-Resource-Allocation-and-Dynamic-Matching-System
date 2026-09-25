from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from engine.models.enums import RequestStatus
from engine.models.location import Location


class RescueRequest(BaseModel):
    """Represents a physical logistics task to transport food from Donor to Agency."""
    id: str = Field(..., description="Unique rescue request ID")
    donation_id: str = Field(..., description="Associated donation ID")
    agency_id: str = Field(..., description="Target recipient agency ID")
    pickup_location: Location = Field(
        ..., description="Pickup location coordinates"
    )
    dropoff_location: Location = Field(
        ..., description="Dropoff location coordinates"
    )
    quantity: float = Field(
        ..., gt=0.0, description="Quantity to transport in kg"
    )
    requires_refrigeration: bool = Field(
        default=False, description="Cold transport requirement"
    )
    pickup_deadline: Optional[datetime] = Field(
        default=None, description="Expiration or pickup deadline"
    )
    dropoff_deadline: Optional[datetime] = Field(
        default=None, description="Delivery completion deadline"
    )
    status: RequestStatus = Field(
        default=RequestStatus.PENDING, description="Current lifecycle state"
    )
