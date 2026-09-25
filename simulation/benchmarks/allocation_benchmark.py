import copy
import time
from typing import List, Tuple

from engine.allocation.fair import FairnessAwareAllocator
from engine.allocation.greedy import GreedyAllocator
from engine.metrics.fairness import allocation_disparity, jains_fairness_index
from simulation.benchmarks.results import BenchmarkResultRow
from simulation.scenarios.scenario import build_allocation_scenario


def run_allocation_benchmark(
    sizes: List[Tuple[int, int]],
    seeds: List[int],
    repetitions: int = 3,
) -> List[BenchmarkResultRow]:
    results: List[BenchmarkResultRow] = []

    allocators = [
        ("Greedy Allocation", GreedyAllocator()),
        ("Fairness-Aware Allocation", FairnessAwareAllocator()),
    ]

    for num_donations, num_agencies in sizes:
        problem_size = num_donations
        print(f"  -> Allocation benchmark size {problem_size} ({num_donations} donations, {num_agencies} agencies)...", flush=True)
        for seed in seeds:
            for rep in range(1, repetitions + 1):
                scenario_seed = seed * 1000 + rep
                scenario = build_allocation_scenario(
                    num_donations=num_donations,
                    num_agencies=num_agencies,
                    seed=scenario_seed,
                )

                for name, allocator in allocators:
                    donations_copy = copy.deepcopy(scenario.donations)
                    agencies_copy = copy.deepcopy(scenario.agencies)

                    t0 = time.perf_counter()
                    batch_res = allocator.allocate(donations_copy, agencies_copy)
                    t1 = time.perf_counter()

                    exec_time_ms = (t1 - t0) * 1000.0

                    total_supply = scenario.total_supply
                    total_allocated = batch_res.total_allocated
                    unmet_demand = batch_res.total_unmet_demand
                    alloc_rate = (
                        total_allocated / total_supply
                        if total_supply > 0
                        else 0.0
                    )
                    jain_val = batch_res.jain_fairness_index
                    disp_val = allocation_disparity(batch_res.agency_ratios)

                    row = BenchmarkResultRow(
                        experiment="allocation",
                        algorithm=name,
                        seed=seed,
                        problem_size=problem_size,
                        repetition=rep,
                        execution_time_ms=exec_time_ms,
                        total_supply=total_supply,
                        total_allocated=total_allocated,
                        unmet_demand=unmet_demand,
                        allocation_rate=alloc_rate,
                        jain_fairness=jain_val,
                        allocation_disparity=disp_val,
                    )
                    results.append(row)

    return results
