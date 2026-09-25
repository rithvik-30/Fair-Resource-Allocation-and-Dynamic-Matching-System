"""Dependencies for FRADMS API."""

from backend.services.allocation_service import AllocationService
from backend.services.dispatch_service import DispatchService
from backend.services.simulation_service import SimulationService


def get_allocation_service() -> AllocationService:
    return AllocationService()


def get_dispatch_service() -> DispatchService:
    return DispatchService()


def get_simulation_service() -> SimulationService:
    return SimulationService()
