from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from engine.models.location import Location


class Volunteer(BaseModel):
    """Represents a volunteer driver available for rescue request dispatch."""
    id: str = Field(..., description="UNique volunteer ID")
    name: str = Field(..., description="Volunteer full name")
    location: Location = Field(..., description="Current location coordinates")
    vehicle_capacity: float = Field(
        ..., ge=0.0, description="Vehicle cargo weight capacity in kg"
    )
    has_refrigeration: bool = Field(
        default=False, description="Whether vehicle has cold transport"
    )
    available_from: Optional[datetime] = Field(
        default=None, description="Start time of availability"
    )
    available_until: Optional[datetime] = Field(
        default=None, description="End time of availability"
    )
    max_travel_distance: Optional[float] = Field(
        default=None, gt=0.0, description="Maximum travel radius limit in km"
    )
    current_workload: int = Field(
        default=0, ge=0, description="Number of currently active assignments"
    )
    total_distance_traveled: float = Field(
        default=0.0, ge=0.0, description="Cumulative distance traveled in km"
    )
    is_available: bool = Field(
        default=True, description="Availability status flag"
    )
