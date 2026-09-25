from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field


class AllocationResult(BaseModel):
    """Represents the outcome of a food allocation decision for a donation-agency pair."""
    donation_id: str = Field(..., description="Target donation ID")
    agency_id: str = Field(..., description="Recipient agency ID")
    allocated_quantity: float = Field(
        ..., ge=0.0, description="Allocated food quantity in kg"
    )
    allocated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Allocation decision timestamp",
    )
    explanation: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata explaining allocation rationale",
    )
