from fastapi import APIRouter, Depends, HTTPException, status
from backend.api.schemas.allocation import (
    AllocationComparisonResponse,
    AllocationRequest,
    AllocationResponse,
)
from backend.dependencies import get_allocation_service
from backend.services.allocation_service import AllocationService

router = APIRouter(prefix="/api/v1/allocation", tags=["Allocation Engine"])


@router.post(
    "/greedy",
    response_model=AllocationResponse,
    summary="Execute Greedy Food Resource Allocation",
)
def allocate_greedy(
    payload: AllocationRequest,
    service: AllocationService = Depends(get_allocation_service),
):
    if not payload.donations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donations list cannot be empty.",
        )
    if not payload.agencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agencies list cannot be empty.",
        )
    return service.run_greedy(payload.donations, payload.agencies)


@router.post(
    "/fair",
    response_model=AllocationResponse,
    summary="Execute Fairness-Aware Food Resource Allocation",
)
def allocate_fair(
    payload: AllocationRequest,
    service: AllocationService = Depends(get_allocation_service),
):
    if not payload.donations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donations list cannot be empty.",
        )
    if not payload.agencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agencies list cannot be empty.",
        )
    return service.run_fair(payload.donations, payload.agencies)


@router.post(
    "/compare",
    response_model=AllocationComparisonResponse,
    summary="Compare Greedy vs Fairness-Aware Allocation Algorithms",
)
def compare_allocation(
    payload: AllocationRequest,
    service: AllocationService = Depends(get_allocation_service),
):
    if not payload.donations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donations list cannot be empty.",
        )
    if not payload.agencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agencies list cannot be empty.",
        )
    return service.run_comparison(payload.donations, payload.agencies)
