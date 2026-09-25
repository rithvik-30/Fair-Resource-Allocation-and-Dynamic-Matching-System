from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from engine.models.agency import Agency
from engine.models.donation import Donation
from engine.models.allocation_result import AllocationResult


class AllocationRequest(BaseModel):
    donations: List[Donation] = Field(
        ..., description="List of available food donations to allocate."
    )
    agencies: List[Agency] = Field(
        ..., description="List of recipient agencies demanding resources."
    )


class AllocationResponse(BaseModel):
    algorithm: str = Field(..., description="Name of the allocation algorithm used.")
    total_supply: float = Field(..., description="Aggregate supply available across donations.")
    total_allocated: float = Field(..., description="Aggregate quantity successfully allocated.")
    unmet_demand: float = Field(..., description="Remaining unfulfilled demand across agencies.")
    unused_supply: float = Field(..., description="Remaining unallocated donation supply.")
    allocation_rate: float = Field(..., description="Ratio of total allocated food to total supply.")
    jain_fairness_index: float = Field(..., description="Jain's Fairness Index (0.0 to 1.0).")
    allocation_disparity: float = Field(..., description="Disparity ratio between highest and lowest agency fulfillment.")
    execution_time_ms: float = Field(..., description="Algorithm execution runtime in milliseconds.")
    allocations: List[AllocationResult] = Field(..., description="List of individual allocation decisions.")
    agency_ratios: Dict[str, float] = Field(..., description="Fulfillment ratio for each agency.")


class AllocationComparisonResponse(BaseModel):
    greedy: AllocationResponse = Field(..., description="Results from Greedy Allocation Algorithm.")
    fairness_aware: AllocationResponse = Field(..., description="Results from Fairness-Aware Allocation Algorithm.")
    comparison_summary: Dict[str, Any] = Field(..., description="Comparative metrics summary.")
