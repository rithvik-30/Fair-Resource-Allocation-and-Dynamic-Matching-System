import copy
from datetime import datetime, timezone
import time
from typing import List

from engine.dispatch.batch_matching import BatchBipartiteDispatcher
from engine.dispatch.nearest import NearestVolunteerDispatcher
from engine.dispatch.scored import ScoreBasedDispatcher
from engine.metrics.dispatch import (
    compute_assignment_rate,
    compute_max_workload,
    compute_workload_distribution,
    compute_workload_variance,
)
from simulation.benchmarks.results import BenchmarkResultRow
from simulation.scenarios.scenario import build_dispatch_scenario


def run_dispatch_benchmark(
    sizes: List[int],
    seeds: List[int],
    repetitions: int = 3,
) -> List[BenchmarkResultRow]:
    results: List[BenchmarkResultRow] = []

    dispatchers = [
        ("Nearest Volunteer Greedy", NearestVolunteerDispatcher()),
        ("Score-Based Dispatch", ScoreBasedDispatcher()),
        ("Batch Bipartite Matching", BatchBipartiteDispatcher()),
    ]

    base_time = datetime(2026, 9, 25, 10, 0, 0, tzinfo=timezone.utc)

    for n in sizes:
        num_requests = n
        num_volunteers = n
        problem_size = n
        print(f"  -> Dispatch benchmark size {problem_size} ({num_requests} reqs, {num_volunteers} vols)...", flush=True)

        for seed in seeds:
            for rep in range(1, repetitions + 1):
                scenario_seed = seed * 1000 + rep
                scenario = build_dispatch_scenario(
                    num_requests=num_requests,
                    num_volunteers=num_volunteers,
                    seed=scenario_seed,
                )

                for name, dispatcher in dispatchers:
                    reqs_copy = copy.deepcopy(scenario.requests)
                    vols_copy = copy.deepcopy(scenario.volunteers)

                    t0 = time.perf_counter()
                    batch_res = dispatcher.dispatch(
                        requests=reqs_copy,
                        volunteers=vols_copy,
                        current_time=base_time,
                    )
                    t1 = time.perf_counter()

                    exec_time_ms = (t1 - t0) * 1000.0

                    assigned_cnt = batch_res.total_assigned
                    unassigned_cnt = batch_res.total_unassigned
                    assign_rate = compute_assignment_rate(
                        assigned_cnt, num_requests
                    )
                    total_dist = batch_res.total_distance_km
                    avg_dist = batch_res.average_distance_km

                    workload_dist = compute_workload_distribution(
                        vols_copy, batch_res.matches
                    )
                    wl_var = compute_workload_variance(workload_dist)
                    max_wl = compute_max_workload(workload_dist)

                    row = BenchmarkResultRow(
                        experiment="dispatch",
                        algorithm=name,
                        seed=seed,
                        problem_size=problem_size,
                        repetition=rep,
                        execution_time_ms=exec_time_ms,
                        requests_count=num_requests,
                        volunteers_count=num_volunteers,
                        assigned_requests=assigned_cnt,
                        unassigned_requests=unassigned_cnt,
                        assignment_rate=assign_rate,
                        total_distance_km=total_dist,
                        average_distance_km=avg_dist,
                        workload_variance=wl_var,
                        max_workload=max_wl,
                    )
                    results.append(row)

    return results
