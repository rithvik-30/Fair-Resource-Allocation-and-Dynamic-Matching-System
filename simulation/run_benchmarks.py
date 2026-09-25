import argparse
import os
import sys
from typing import List, Tuple

from simulation.analysis.aggregate import (
    aggregate_allocation_results,
    aggregate_dispatch_results,
    save_aggregated_to_csv,
)
from simulation.analysis.plots import generate_all_plots
from simulation.benchmarks.allocation_benchmark import run_allocation_benchmark
from simulation.benchmarks.dispatch_benchmark import run_dispatch_benchmark
from simulation.benchmarks.results import load_results_from_csv, save_results_to_csv


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run reproducible benchmarks for Fair Food Resource Allocation and Dynamic Volunteer Dispatch."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run a quick smoke benchmark with small sizes (10, 25) and single seed.",
    )
    parser.add_argument(
        "--sizes",
        type=str,
        default="10,25,50,100",
        help="Comma-separated problem sizes (default: 10,25,50,100). Larger sizes like 250,500,1000 can also be passed.",
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default="42,43,44",
        help="Comma-separated random seeds (default: 42,43,44).",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=3,
        help="Number of repetitions per seed (default: 3).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="simulation/results",
        help="Directory to save CSV results and plots (default: simulation/results).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.quick:
        sizes_alloc = [(10, 5), (25, 12)]
        sizes_disp = [10, 25]
        seeds = [42]
        reps = 1
        print("=== RUNNING QUICK SMOKE BENCHMARK ===")
    else:
        parsed_sizes = [int(s.strip()) for s in args.sizes.split(",") if s.strip()]
        sizes_alloc: List[Tuple[int, int]] = [(n, max(2, n // 2)) for n in parsed_sizes]
        sizes_disp: List[int] = parsed_sizes
        seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
        reps = args.repetitions
        print(f"=== RUNNING BENCHMARK (Sizes: {parsed_sizes}, Seeds: {seeds}, Reps: {reps}) ===")

    output_dir = args.output_dir
    plots_dir = os.path.join(output_dir, "plots")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    print("\n[1/5] Running Fair Food Resource Allocation Benchmark...")
    alloc_rows = run_allocation_benchmark(
        sizes=sizes_alloc, seeds=seeds, repetitions=reps
    )
    alloc_csv = os.path.join(output_dir, "allocation_benchmark.csv")
    save_results_to_csv(alloc_csv, alloc_rows)
    print(f"  -> Saved {len(alloc_rows)} allocation raw result rows to {alloc_csv}")

    print("\n[2/5] Running Dynamic Volunteer Dispatch Benchmark...")
    disp_rows = run_dispatch_benchmark(
        sizes=sizes_disp, seeds=seeds, repetitions=reps
    )
    disp_csv = os.path.join(output_dir, "dispatch_benchmark.csv")
    save_results_to_csv(disp_csv, disp_rows)
    print(f"  -> Saved {len(disp_rows)} dispatch raw result rows to {disp_csv}")

    print("\n[3/5] Aggregating Benchmark Results...")
    alloc_raw_loaded = load_results_from_csv(alloc_csv)
    disp_raw_loaded = load_results_from_csv(disp_csv)

    alloc_agg = aggregate_allocation_results(alloc_raw_loaded)
    disp_agg = aggregate_dispatch_results(disp_raw_loaded)

    alloc_agg_csv = os.path.join(output_dir, "allocation_aggregated.csv")
    disp_agg_csv = os.path.join(output_dir, "dispatch_aggregated.csv")

    save_aggregated_to_csv(alloc_agg_csv, alloc_agg)
    save_aggregated_to_csv(disp_agg_csv, disp_agg)
    print(f"  -> Saved aggregated allocation results to {alloc_agg_csv}")
    print(f"  -> Saved aggregated dispatch results to {disp_agg_csv}")

    print("\n[4/5] Generating Matplotlib Plots...")
    plots_created = generate_all_plots(alloc_agg, disp_agg, plots_dir)
    print(f"  -> Saved {len(plots_created)} plots in {plots_dir}")

    print("\n[5/5] BENCHMARK SUMMARY TABLE")
    print("=" * 80)
    print("ALLOCATION ENGINE SUMMARY (Mean Runtime & Jain Fairness):")
    print(f"{'Algorithm':<30} | {'Size':<6} | {'Runtime (ms)':<14} | {'Alloc Rate':<12} | {'Jain Index':<10}")
    print("-" * 80)
    for r in alloc_agg:
        print(
            f"{r['algorithm']:<30} | {r['problem_size']:<6} | "
            f"{r['mean_runtime_ms']:<14.3f} | {r['mean_allocation_rate']:<12.4f} | "
            f"{r['mean_jain_fairness']:<10.4f}"
        )

    print("\n" + "=" * 80)
    print("DISPATCH ENGINE SUMMARY (Mean Runtime, Assign Rate, & Distance):")
    print(f"{'Algorithm':<26} | {'Size':<6} | {'Runtime (ms)':<14} | {'Assign Rate':<12} | {'Tot Dist (km)':<14} | {'WL Var':<8}")
    print("-" * 80)
    for r in disp_agg:
        print(
            f"{r['algorithm']:<26} | {r['problem_size']:<6} | "
            f"{r['mean_runtime_ms']:<14.3f} | {r['mean_assignment_rate']:<12.4f} | "
            f"{r['mean_total_distance_km']:<14.2f} | {r['mean_workload_variance']:<8.4f}"
        )
    print("=" * 80)
    print("\nBenchmark completed successfully!\n")


if __name__ == "__main__":
    main()
