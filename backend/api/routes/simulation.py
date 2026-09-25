from fastapi import APIRouter, Depends
from backend.api.schemas.simulation import (
    QuickSimulationRequest,
    QuickSimulationResponse,
)
from backend.dependencies import get_simulation_service
from backend.services.simulation_service import SimulationService

router = APIRouter(prefix="/api/v1/simulation", tags=["Simulation Suite"])


@router.post(
    "/quick",
    response_model=QuickSimulationResponse,
    summary="Execute Quick Simulation Benchmark",
)
def run_quick_simulation(
    payload: QuickSimulationRequest = QuickSimulationRequest(),
    service: SimulationService = Depends(get_simulation_service),
):
    return service.run_quick_simulation(
        sizes=payload.sizes,
        seed=payload.seed,
        repetitions=payload.repetitions,
    )
