import csv
from dataclasses import asdict, dataclass
import os
from typing import Any, Dict, List, Optional


@dataclass
class BenchmarkResultRow:
    experiment: str
    algorithm: str
    seed: int
    problem_size: int
    repetition: int
    execution_time_ms: float
    total_supply: Optional[float] = None
    total_allocated: Optional[float] = None
    unmet_demand: Optional[float] = None
    allocation_rate: Optional[float] = None
    jain_fairness: Optional[float] = None
    allocation_disparity: Optional[float] = None
    requests_count: Optional[int] = None
    volunteers_count: Optional[int] = None
    assigned_requests: Optional[int] = None
    unassigned_requests: Optional[int] = None
    assignment_rate: Optional[float] = None
    total_distance_km: Optional[float] = None
    average_distance_km: Optional[float] = None
    workload_variance: Optional[float] = None
    max_workload: Optional[int] = None


def save_results_to_csv(filepath: str, rows: List[BenchmarkResultRow]) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not rows:
        return

    fieldnames = list(asdict(rows[0]).keys())
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def load_results_from_csv(filepath: str) -> List[Dict[str, Any]]:
    results = []
    if not os.path.exists(filepath):
        return results

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            converted = {}
            for k, v in row.items():
                if v == "" or v is None:
                    converted[k] = None
                elif k in (
                    "seed",
                    "problem_size",
                    "repetition",
                    "requests_count",
                    "volunteers_count",
                    "assigned_requests",
                    "unassigned_requests",
                    "max_workload",
                ):
                    converted[k] = int(v)
                elif k in (
                    "execution_time_ms",
                    "total_supply",
                    "total_allocated",
                    "unmet_demand",
                    "allocation_rate",
                    "jain_fairness",
                    "allocation_disparity",
                    "assignment_rate",
                    "total_distance_km",
                    "average_distance_km",
                    "workload_variance",
                ):
                    converted[k] = float(v)
                else:
                    converted[k] = v
            results.append(converted)
    return results
