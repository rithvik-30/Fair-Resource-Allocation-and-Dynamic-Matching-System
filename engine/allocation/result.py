from typing import Dict, List
from pydantic import BaseModel, Field
from engine.models.allocation_result import AllocationResult


class AllocationBatchResult(BaseModel):
    """Aggregate result representation for a batch resource allocation execution."""
    algorithm_name: str = Field(
        ..., description="Name of the allocation algorithm used"
    )
    allocations: List[AllocationResult] = Field(
        default_factory=list, description="List of individual allocation items"
    )
    total_allocated: float = Field(
        ..., ge=0.0, description="Total food quantity allocation in kg"
    )
    total_unmet_demand: float = Field(
        ..., ge=0.0, description="Unmet_demand in kg"
    )
    total_unused_supply: float = Field(
        ..., ge=0.0, description="Unallocated supply in kg"
    )
    execution_time_ms: float = Field(
        ..., ge=0.0, description="Execution runtime in milliseconds"
    )
    agency_ratios: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-agency allocation satisfaction ratios",
    )
    jain_fairness_index: float = Field(
        ..., ge=0.0, le=1.0, description="Jain's Fairness Index score"
    )
