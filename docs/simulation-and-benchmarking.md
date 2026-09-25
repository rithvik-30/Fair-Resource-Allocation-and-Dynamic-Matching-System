# Simulation & Benchmarking Framework

## 1. Overview & Objectives

In real-world food rescue logistics, live operational data is often fragmented, noisy, or limited in scale. To rigorously evaluate the scalability, efficiency, and trade-offs of our allocation and dispatch algorithms, a controlled **Simulation and Benchmarking System** is essential.

The benchmark answers core computational questions:
- How do execution runtimes scale as problem sizes increase from 10 to 1,000 items?
- How does allocation fairness (measured via Jain's Fairness Index) compare between greedy and multi-objective algorithms under constrained supply?
- How do dynamic dispatch algorithms trade off total travel distance, volunteer workload variance, and request assignment rates?

> **Important**: This framework measures empirical performance under controlled synthetic workloads. Benchmark results reflect algorithmic trade-offs under specified distribution parameters and should not be blindly generalized to all real-world logistics networks.

---

## 2. Summary of Experiments

| Experiment | Evaluated Algorithms | Primary Metrics Recorded |
| :--- | :--- | :--- |
| **Allocation Engine** | `Greedy Allocation`<br>`Fairness-Aware Allocation` | Execution Time (ms), Total Supply, Total Allocated, Unmet Demand, Allocation Rate, Jain Fairness Index, Allocation Disparity |
| **Dispatch Engine** | `Nearest Volunteer Greedy`<br>`Score-Based Dispatch`<br>`Batch Bipartite Matching` | Execution Time (ms), Total Requests, Volunteers, Assigned Requests, Assignment Rate, Total Distance (km), Average Distance (km), Workload Variance, Max Workload |

---

## 3. Synthetic Data Generation & Reproducibility

All synthetic scenarios are generated using isolated pseudo-random number generators seeded by fixed integer seeds (`SEEDS = [42, 43, 44]`). Given identical seed and size parameters, data generators yield 100% deterministic, reproducible workloads.

### A. Location Generation
- Bounding Box: San Francisco Metropolitan Region (`37.70° N` to `37.85° N`, `-122.52° W` to `-122.35° W`).
- Coordinates generated uniformly within the bounding box for donors, recipient agencies, request pickups, request dropoffs, and volunteer starting locations.

### B. Allocation Workload Generation
- **Donations**: Quantity (20.0 to 500.0 kg), food type (`Produce`, `Dairy`, `Prepared Meals`, etc.), refrigeration requirements (30% probability), expiration timelines (6 to 72 hours).
- **Recipient Agencies**: Demand (50.0 to 800.0 kg), storage capacity, priority score (1 to 5), historical allocations (0.0 to 1,500.0 kg), refrigeration capabilities (50% probability).
- Controlled variation in demand, priority, and allocation history ensures fairness metrics measure non-trivial distributions.

### C. Dispatch Workload Generation
- **Rescue Requests**: Pickup & dropoff locations, food quantities, refrigeration flags, time windows / deadlines.
- **Volunteers**: Location, vehicle capacity (50 to 500 kg), refrigeration support (35% probability), max travel distance limits (15 to 100 km), and initial workload variation (0 to 3 active tasks).

---

## 4. Benchmark Methodology & Execution Scenarios

### Benchmark Sizes
Controlled problem sizes span orders of magnitude:
- **Allocation**: `10, 25, 50, 100, 250, 500, 1000` donations (mapped to matching scaled agency sets).
- **Dispatch**: `10, 25, 50, 100, 250, 500, 1000` requests and volunteers.

### Runtime Isolation
To ensure precise measurements:
- **Scenario data generation time is strictly excluded** from algorithm execution timing.
- Runtimes are measured using `time.perf_counter()` around the algorithm's pure `.allocate()` or `.dispatch()` execution.
- Deep copies of input models are passed to each algorithm to prevent state mutation leaks between repeated runs.

### Aggregation Statistics
Every benchmark run is repeated across 3 seeds with 3 repetitions per seed (9 iterations per problem size/algorithm combination). Results are aggregated by computing:
- **Mean Runtime** & **Median Runtime** (ms)
- **Standard Deviation** (ms)
- **Mean Fairness Index** & **Mean Allocation Rate**
- **Mean Assignment Rate**, **Mean Total Distance**, and **Mean Workload Variance**

---

## 5. Visualization & Analysis Pipeline

The benchmark automatically generates 7 Matplotlib visualization plots stored in `simulation/results/plots/`:

1. `allocation_runtime_vs_size.png`: Execution time scaling for allocation algorithms.
2. `allocation_rate_vs_size.png`: Percentage of food supply successfully allocated.
3. `allocation_fairness_vs_size.png`: Jain's Fairness Index across problem sizes.
4. `dispatch_runtime_vs_size.png`: Execution time scaling for volunteer dispatch algorithms.
5. `dispatch_assignment_rate_vs_size.png`: Proportion of rescue requests matched to volunteers.
6. `dispatch_total_distance_vs_size.png`: Aggregate travel distance (km) across matches.
7. `dispatch_workload_variance_vs_size.png`: Balance of task distribution among volunteers.

---

## 6. How to Run Benchmarks

Run the complete benchmark, aggregate results, and render plots:

```bash
python -m simulation.run_benchmarks
```

Run a quick smoke test for verification:

```bash
python -m simulation.run_benchmarks --quick
```

Custom CLI Options:

```bash
python -m simulation.run_benchmarks --sizes 10,50,200 --seeds 42,43 --repetitions 5 --output-dir simulation/results
```
