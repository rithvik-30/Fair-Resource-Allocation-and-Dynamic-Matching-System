from typing import Dict, List, Union
from engine.models.agency import Agency
from engine.models.allocation_result import AllocationResult


def compute_allocation_ratios(
    agencies: List[Agency],
    allocations: List[AllocationResult],
) -> Dict[str, float]:
    """Compute per-agency food demand satisfaction ratios.
    Returns dictionary mapping agency_id to satisfaction ratio."""
    new_allocations_map: Dict[str, float] = {}
    for alloc in allocations:
        new_allocations_map[alloc.agency_id] = (
            new_allocations_map.get(alloc.agency_id, 0.0)
            + alloc.allocated_quantity
        )

    ratios: Dict[str, float] = {}
    for agency in agencies:
        new_alloc = new_allocations_map.get(agency.id, 0.0)
        total_received = agency.historical_allocations + new_alloc
        if agency.demands > 0:
            ratios[agency.id] = min(1.0, total_received / agency.demands)
        else:
            ratios[agency.id] = 1.0 if total_received >= 0 else 0.0

    return ratios


def jains_fairness_index(
    values: Union[List[float], Dict[str, float]],
) -> float:
    """Compute Jain's Fairness Index for a set of satisfaction ratios."""
    if isinstance(values, dict):
        x = list(values.values())
    else:
        x = list(values)

    n = len(x)
    if n == 0:
        return 1.0

    sum_x = sum(x)
    sum_sq_x = sum(val**2 for val in x)

    if sum_sq_x == 0.0:
        return 1.0

    jain_index = (sum_x**2) / (n * sum_sq_x)
    return max(0.0, min(1.0, jain_index))


def allocation_disparity(
    values: Union[List[float], Dict[str, float]],
) -> float:
    """Compute absolute allocation disparity (max ratio - min ratio)."""
    if isinstance(values, dict):
        x = list(values.values())
    else:
        x = list(values)

    if not x:
        return 0.0

    return max(x) - min(x)
