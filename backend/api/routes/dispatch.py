from fastapi import APIRouter, Depends, HTTPException, status
from backend.api.schemas.dispatch import (
    DispatchComparisonResponse,
    DispatchRequest,
    DispatchResponse,
)
from backend.dependencies import get_dispatch_service
from backend.services.dispatch_service import DispatchService

router = APIRouter(prefix="/api/v1/dispatch", tags=["Dispatch Engine"])


@router.post(
    "/nearest",
    response_model=DispatchResponse,
    summary="Execute Nearest Volunteer Greedy Dispatch",
)
def dispatch_nearest(
    payload: DispatchRequest,
    service: DispatchService = Depends(get_dispatch_service),
):
    if not payload.requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rescue requests list cannot be empty.",
        )
    if not payload.volunteers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteers list cannot be empty.",
        )
    return service.run_nearest(payload.requests, payload.volunteers, payload.current_time)


@router.post(
    "/scored",
    response_model=DispatchResponse,
    summary="Execute Multi-Criteria Score-Based Dispatch",
)
def dispatch_scored(
    payload: DispatchRequest,
    service: DispatchService = Depends(get_dispatch_service),
):
    if not payload.requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rescue requests list cannot be empty.",
        )
    if not payload.volunteers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteers list cannot be empty.",
        )
    return service.run_scored(payload.requests, payload.volunteers, payload.current_time)


@router.post(
    "/batch",
    response_model=DispatchResponse,
    summary="Execute Batch Bipartite Matching Dispatch",
)
def dispatch_batch(
    payload: DispatchRequest,
    service: DispatchService = Depends(get_dispatch_service),
):
    if not payload.requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rescue requests list cannot be empty.",
        )
    if not payload.volunteers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteers list cannot be empty.",
        )
    return service.run_batch(payload.requests, payload.volunteers, payload.current_time)


@router.post(
    "/compare",
    response_model=DispatchComparisonResponse,
    summary="Compare Nearest vs Scored vs Batch Bipartite Matching Strategies",
)
def compare_dispatch(
    payload: DispatchRequest,
    service: DispatchService = Depends(get_dispatch_service),
):
    if not payload.requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rescue requests list cannot be empty.",
        )
    if not payload.volunteers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Volunteers list cannot be empty.",
        )
    return service.run_comparison(payload.requests, payload.volunteers, payload.current_time)
