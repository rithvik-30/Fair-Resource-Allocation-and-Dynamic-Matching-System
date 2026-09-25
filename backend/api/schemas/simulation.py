from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class QuickSimulationRequest(BaseModel):
    sizes: Optional[List[int]] = Field(
        [10, 25, 50], description="Problem sizes to benchmark in quick mode."
    )
    seed: Optional[int] = Field(
        42, description="Random seed for reproducible scenario generation."
    )
    repetitions: Optional[int] = Field(
        1, description="Number of repetitions per seed/size."
    )


class QuickSimulationResponse(BaseModel):
    status: str = Field(..., description="Execution status.")
    allocation_results: List[Dict[str, Any]] = Field(
        ..., description="Aggregated allocation benchmark metrics."
    )
    dispatch_results: List[Dict[str, Any]] = Field(
        ..., description="Aggregated dispatch benchmark metrics."
    )
    plots_generated: List[str] = Field(
        ..., description="Paths or basenames of generated visualization plots."
    )
