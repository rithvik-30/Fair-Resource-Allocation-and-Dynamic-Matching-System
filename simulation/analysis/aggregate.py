import csv
import math
import os
from typing import Any, Dict, List, Optional, Tuple


def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _median(values: List[float]) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2.0


def _std(values: List[float]) -> float:
    if len(values) <= 1:
        return 0.0
    m = _mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def aggregate_allocation_results(
    raw_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for r in raw_results:
        if r.get("experiment") != "allocation":
            continue
        key = (str(r["algorithm"]), int(r["problem_size"]))
        if key not in groups:
            groups[key] = []
        groups[key].append(r)

    aggregated = []
    for (algorithm, problem_size), rows in sorted(groups.items()):
        runtimes = [float(r["execution_time_ms"]) for r in rows]
        alloc_rates = [float(r["allocation_rate"]) for r in rows]
        jains = [float(r["jain_fairness"]) for r in rows]
        disparities = [float(r["allocation_disparity"]) for r in rows]
        unmet = [float(r["unmet_demand"]) for r in rows]
        allocated = [float(r["total_allocated"]) for r in rows]

        agg_row = {
            "experiment": "allocation",
            "algorithm": algorithm,
            "problem_size": problem_size,
            "sample_count": len(rows),
            "mean_runtime_ms": round(_mean(runtimes), 3),
            "median_runtime_ms": round(_median(runtimes), 3),
            "std_runtime_ms": round(_std(runtimes), 3),
            "mean_allocation_rate": round(_mean(alloc_rates), 4),
            "mean_jain_fairness": round(_mean(jains), 4),
            "mean_allocation_disparity": round(_mean(disparities), 4),
            "mean_unmet_demand": round(_mean(unmet), 2),
            "mean_total_allocated": round(_mean(allocated), 2),
        }
        aggregated.append(agg_row)

    return aggregated


def aggregate_dispatch_results(
    raw_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for r in raw_results:
        if r.get("experiment") != "dispatch":
            continue
        key = (str(r["algorithm"]), int(r["problem_size"]))
        if key not in groups:
            groups[key] = []
        groups[key].append(r)

    aggregated = []
    for (algorithm, problem_size), rows in sorted(groups.items()):
        runtimes = [float(r["execution_time_ms"]) for r in rows]
        assign_rates = [float(r["assignment_rate"]) for r in rows]
        tot_dists = [float(r["total_distance_km"]) for r in rows]
        avg_dists = [float(r["average_distance_km"]) for r in rows]
        wl_vars = [float(r["workload_variance"]) for r in rows]
        assigned_cnts = [float(r["assigned_requests"]) for r in rows]

        agg_row = {
            "experiment": "dispatch",
            "algorithm": algorithm,
            "problem_size": problem_size,
            "sample_count": len(rows),
            "mean_runtime_ms": round(_mean(runtimes), 3),
            "median_runtime_ms": round(_median(runtimes), 3),
            "std_runtime_ms": round(_std(runtimes), 3),
            "mean_assignment_rate": round(_mean(assign_rates), 4),
            "mean_total_distance_km": round(_mean(tot_dists), 2),
            "mean_average_distance_km": round(_mean(avg_dists), 2),
            "mean_workload_variance": round(_mean(wl_vars), 4),
            "mean_assigned_requests": round(_mean(assigned_cnts), 1),
        }
        aggregated.append(agg_row)

    return aggregated


def save_aggregated_to_csv(filepath: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
