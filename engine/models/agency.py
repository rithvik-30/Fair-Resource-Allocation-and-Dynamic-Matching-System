from pydantic import BaseModel, Field, field_validator
from engine.models.location import Location


class Agency(BaseModel):
    """Represents a recipient beneficiary organization (food bank, shelter)."""
    id: str = Field(..., description="Unique agency ID")
    name: str = Field(..., description="Agency organization name")
    location: Location = Field(..., description="Physical location coordinates")
    storage_capacity: float = Field(
        ..., ge=0.0, description="Total storage capacity in kg"
    )
    current_inventory: float = Field(
        default=0.0, ge=0.0, description="Current food inventory in kg"
    )
    demands: float = Field(
        ..., ge=0.0, description="Requested food demand in kg"
    )
    priority_score: float = Field(
        default=1.0,
        ge=1.0,
        le=10.0,
        description="Priority weight score (1.0 - 10.0)",
    )
    historical_allocations: float = Field(
        default=0.0,
        ge=0.0,
        description="Cumulative past food allocated over evaluation window (kg)",
    )
    refrigeration_capable: bool = Field(
        default=False, description="Whether cold storage capability is present"
    )

    @field_validator("current_inventory")
    @classmethod
    def validate_inventory(cls, v: float, info) -> float:
        storage_cap = info.data.get("storage_capacity")
        if storage_cap is not None and v > storage_cap:
            raise ValueError(
                f"Current inventory ({v} kg) cannot exceed total storage capacity ({storage_cap} kg)"
            )
        return v

    @property
    def available_capacity(self) -> float:
        """Returns remaining available storage capacity in kg."""
        return max(0.0, self.storage_capacity - self.current_inventory)

    @property
    def unmet_demand(self) -> float:
        """Returns current unmet food demand in kg."""
        return max(0.0, self.demands)
