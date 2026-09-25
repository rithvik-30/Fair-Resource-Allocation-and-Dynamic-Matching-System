from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


class DispatchRequest(BaseModel):
    requests: List[RescueRequest] = Field(
        ..., description="List of pending food rescue requests."
    )
    volunteers: List[Volunteer] = Field(
        ..., description="List of active volunteers available for dispatch."
    )
    current_time: Optional[datetime] = Field(
        None, description="Optional simulation current timestamp for deadline evaluation."
    )


class DispatchMatchResponse(BaseModel):
    request_id: str = Field(..., description="ID of the assigned rescue request.")
    volunteer_id: str = Field(..., description="ID of the assigned volunteer.")
    pickup_distance_km: float = Field(..., description="Distance from volunteer location to pickup location.")
    dropoff_distance_km: float = Field(..., description="Distance from pickup location to dropoff location.")
    total_distance_km: float = Field(..., description="Total travel distance for the rescue trip.")
    is_feasible: bool = Field(..., description="Whether the match satisfies all constraints.")
    feasibility_reasons: List[str] = Field(..., description="Audit reasons explaining feasibility checks.")


class DispatchResponse(BaseModel):
    algorithm: str = Field(..., description="Name of the dispatch strategy used.")
    assigned_requests_count: int = Field(..., description="Number of requests assigned to volunteers.")
    unassigned_requests_count: int = Field(..., description="Number of unassigned requests.")
    assignment_rate: float = Field(..., description="Ratio of assigned requests to total requests.")
    total_distance_km: float = Field(..., description="Total distance traveled across all matches.")
    average_distance_km: float = Field(..., description="Average distance traveled per assigned match.")
    workload_variance: float = Field(..., description="Variance in assigned workloads across volunteers.")
    max_workload: int = Field(..., description="Maximum workload assigned to any single volunteer.")
    execution_time_ms: float = Field(..., description="Algorithm execution runtime in milliseconds.")
    matches: List[DispatchMatchResponse] = Field(..., description="Detailed match decisions.")
    unassigned_request_ids: List[str] = Field(..., description="IDs of requests that could not be matched.")


class DispatchComparisonResponse(BaseModel):
    nearest: DispatchResponse = Field(..., description="Results from Nearest Volunteer Greedy Dispatch.")
    scored: DispatchResponse = Field(..., description="Results from Multi-Criteria Score-Based Dispatch.")
    batch_bipartite: DispatchResponse = Field(..., description="Results from Batch Bipartite Matching Dispatch.")
    comparison_summary: Dict[str, Any] = Field(..., description="Comparative performance metrics summary.")
