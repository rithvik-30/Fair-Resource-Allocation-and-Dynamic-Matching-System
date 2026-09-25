from typing import Dict, List
from engine.dispatch.result import DispatchMatchDetails
from engine.models.volunteer import Volunteer


def compute_total_distance(matches: List[DispatchMatchDetails]) -> float:
    return sum(m.pickup_distance_km for m in matches)


def compute_average_distance(matches: List[DispatchMatchDetails]) -> float:
    if not matches:
        return 0.0
    return compute_total_distance(matches) / len(matches)


def compute_assignment_rate(assigned: int, total_requests: int) -> float:
    if total_requests <= 0:
        return 1.0
    return assigned / total_requests


def compute_workload_distribution(
    volunteers: List[Volunteer],
    matches: List[DispatchMatchDetails],
) -> Dict[str, int]:
    workloads = {v.id: v.current_workload for v in volunteers}
    for m in matches:
        if m.volunteer_id in workloads:
            workloads[m.volunteer_id] += 1
        else:
            workloads[m.volunteer_id] = 1
    return workloads


def compute_workload_variance(workloads: Dict[str, int]) -> float:
    if not workloads:
        return 0.0
    vals = list(workloads.values())
    mean = sum(vals) / len(vals)
    return sum((x - mean) ** 2 for x in vals) / len(vals)


def compute_max_workload(workloads: Dict[str, int]) -> int:
    if not workloads:
        return 0
    return max(workloads.values())
