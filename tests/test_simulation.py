import os
import pytest

from engine.models.location import Location
from simulation.generators.locations import DEFAULT_BOUNDING_BOX, generate_locations
from simulation.generators.allocation_data import generate_allocation_scenario
from simulation.generators.dispatch_data import generate_dispatch_scenario
from simulation.scenarios.scenario import build_allocation_scenario, build_dispatch_scenario
from simulation.benchmarks.allocation_benchmark import run_allocation_benchmark
from simulation.benchmarks.dispatch_benchmark import run_dispatch_benchmark
from simulation.analysis.aggregate import (
    aggregate_allocation_results,
    aggregate_dispatch_results,
    _mean,
    _median,
    _std,
)
from simulation.analysis.plots import generate_all_plots
from simulation.benchmarks.results import load_results_from_csv, save_results_to_csv, BenchmarkResultRow


def test_locations_seed_determinism_and_bounds():
    locs1 = generate_locations(10, seed=42)
    locs2 = generate_locations(10, seed=42)
    locs3 = generate_locations(10, seed=99)

    assert locs1 == locs2
    assert locs1 != locs3

    min_lat, max_lat, min_lon, max_lon = DEFAULT_BOUNDING_BOX
    for loc in locs1:
        assert min_lat <= loc.latitude <= max_lat
        assert min_lon <= loc.longitude <= max_lon


def test_allocation_generator_determinism_and_ranges():
    d1, a1 = generate_allocation_scenario(5, 3, seed=100)
    d2, a2 = generate_allocation_scenario(5, 3, seed=100)
    d3, a3 = generate_allocation_scenario(5, 3, seed=200)

    assert len(d1) == 5
    assert len(a1) == 3
    assert d1[0].id == d2[0].id
    assert d1[0].quantity == d2[0].quantity
    assert d1[0].id != d3[0].id or d1[0].quantity != d3[0].quantity

    for d in d1:
        assert 20.0 <= d.quantity <= 500.0
        assert d.food_type in ["Produce", "Dairy", "Prepared Meals", "Bakery", "Canned Goods"]

    for a in a1:
        assert 50.0 <= a.demands <= 800.0
        assert a.storage_capacity >= 0.0
        assert 1.0 <= a.priority_score <= 5.0


def test_dispatch_generator_determinism_and_ranges():
    r1, v1 = generate_dispatch_scenario(6, 4, seed=123)
    r2, v2 = generate_dispatch_scenario(6, 4, seed=123)
    r3, v3 = generate_dispatch_scenario(6, 4, seed=456)

    assert len(r1) == 6
    assert len(v1) == 4
    assert r1[0].id == r2[0].id
    assert r1[0].quantity == r2[0].quantity
    assert v1[0].id == v2[0].id

    for r in r1:
        assert 10.0 <= r.quantity <= 250.0
        assert r.pickup_deadline < r.dropoff_deadline

    for v in v1:
        assert v.vehicle_capacity in [50.0, 100.0, 150.0, 250.0, 500.0]
        assert v.current_workload >= 0


def test_empty_and_small_scenarios():
    d_empty, a_empty = generate_allocation_scenario(0, 0, seed=1)
    assert len(d_empty) == 0
    assert len(a_empty) == 0

    r_empty, v_empty = generate_dispatch_scenario(0, 0, seed=1)
    assert len(r_empty) == 0
    assert len(v_empty) == 0


def test_benchmark_execution_and_result_fields():
    alloc_rows = run_allocation_benchmark(sizes=[(5, 3)], seeds=[42], repetitions=1)
    assert len(alloc_rows) == 2
    row = alloc_rows[0]
    assert row.experiment == "allocation"
    assert row.execution_time_ms >= 0.0
    assert row.allocation_rate is not None
    assert row.jain_fairness is not None

    disp_rows = run_dispatch_benchmark(sizes=[5], seeds=[42], repetitions=1)
    assert len(disp_rows) == 3
    drow = disp_rows[0]
    assert drow.experiment == "dispatch"
    assert drow.execution_time_ms >= 0.0
    assert drow.assignment_rate is not None
    assert drow.total_distance_km is not None


def test_aggregation_correctness():
    values = [10.0, 20.0, 30.0]
    assert _mean(values) == 20.0
    assert _median(values) == 20.0
    assert abs(_std(values) - 10.0) < 1e-5

    raw_alloc = [
        {
            "experiment": "allocation",
            "algorithm": "Greedy Allocation",
            "problem_size": 10,
            "execution_time_ms": 1.0,
            "allocation_rate": 0.8,
            "jain_fairness": 0.9,
            "allocation_disparity": 0.1,
            "unmet_demand": 50.0,
            "total_allocated": 200.0,
        },
        {
            "experiment": "allocation",
            "algorithm": "Greedy Allocation",
            "problem_size": 10,
            "execution_time_ms": 3.0,
            "allocation_rate": 1.0,
            "jain_fairness": 0.9,
            "allocation_disparity": 0.1,
            "unmet_demand": 0.0,
            "total_allocated": 250.0,
        },
    ]
    agg = aggregate_allocation_results(raw_alloc)
    assert len(agg) == 1
    assert agg[0]["mean_runtime_ms"] == 2.0
    assert agg[0]["mean_allocation_rate"] == 0.9


def test_plot_generation_temp_dir(tmp_path):
    alloc_agg = [
        {
            "algorithm": "Greedy Allocation",
            "problem_size": 10,
            "mean_runtime_ms": 1.5,
            "mean_allocation_rate": 0.9,
            "mean_jain_fairness": 0.95,
        },
        {
            "algorithm": "Fairness-Aware Allocation",
            "problem_size": 10,
            "mean_runtime_ms": 2.0,
            "mean_allocation_rate": 0.9,
            "mean_jain_fairness": 0.99,
        },
    ]
    disp_agg = [
        {
            "algorithm": "Nearest Volunteer Greedy",
            "problem_size": 10,
            "mean_runtime_ms": 1.2,
            "mean_assignment_rate": 0.8,
            "mean_total_distance_km": 50.0,
            "mean_workload_variance": 0.5,
        },
        {
            "algorithm": "Batch Bipartite Matching",
            "problem_size": 10,
            "mean_runtime_ms": 3.2,
            "mean_assignment_rate": 0.9,
            "mean_total_distance_km": 40.0,
            "mean_workload_variance": 0.2,
        },
    ]

    out_dir = str(tmp_path / "plots")
    plots = generate_all_plots(alloc_agg, disp_agg, out_dir)
    assert len(plots) == 7
    for p in plots:
        assert os.path.exists(p)
