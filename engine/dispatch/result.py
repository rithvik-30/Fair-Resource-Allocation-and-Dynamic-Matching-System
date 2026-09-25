from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DispatchMatchDetails(BaseModel):
    """Detailed assignment record of a RescueRequest to a Volunteer."""

    request_id: str = Field(..., description="Target RescueRequest ID")
    volunteer_id: str = Field(..., description="Assigned Volunteer ID")
    pickup_distance_km: float = Field(
        ..., ge=0.0, description="Distance from volunteer to pickup location in km"
    )
    delivery_distance_km: float = Field(
        default=0.0,
        ge=0.0,
        description="Distance from pickup to dropoff location in km",
    )
    total_distance_km: float = Field(
        ..., ge=0.0, description="Total travel distance in km"
    )
    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of assignment",
    )
    explanation: Dict[str, Any] = Field(
        default_factory=dict, description="Algorithm justification metadata"
    )


class DispatchBatchResult(BaseModel):
    """Encapsulates the complete results of a batch dispatch run."""

    algorithm_name: str = Field(
        ..., description="Name of the dispatch strategy used"
    )
    matches: List[DispatchMatchDetails] = Field(
        default_factory=list, description="List of successful assignments"
    )
    unassigned_request_ids: List[str] = Field(
        default_factory=list, description="IDs of requests that could not be assigned"
    )
    total_distance_km: float = Field(
        default=0.0, ge=0.0, description="Sum of pickup distances for all assigned matches"
    )
    average_distance_km: float = Field(
        default=0.0, ge=0.0, description="Average pickup distance per assigned request"
    )
    total_assigned: int = Field(
        default=0, ge=0, description="Total number of successfully assigned requests"
    )
    total_unassigned: int = Field(
        default=0, ge=0, description="Total number of unassigned requests"
    )
    workload_variance: float = Field(
        default=0.0, ge=0.0, description="Variance in workload across all volunteers"
    )
    execution_time_ms: float = Field(
        default=0.0, ge=0.0, description="Execution duration in milliseconds"
    )
