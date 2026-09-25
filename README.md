# Fair Resource Allocation and Dynamic Matching System

An algorithmic decision-support system for fair resource allocation and dynamic task matching, applied to food rescue logistics.

---

## Overview

Food rescue organizations need to make two important computational decisions:

1. **Fair Food Resource Allocation**: Determining how surplus food donations should be distributed among recipient agencies with different needs, storage capacities, priorities, and cold-chain requirements.
2. **Dynamic Volunteer Dispatch**: Assigning incoming rescue tasks to available volunteers while considering geographic distance, vehicle capacity, refrigeration compatibility, deadline urgency, and workload equity.

This repository models these decisions as formal algorithmic problems, providing clean, deterministic, and offline-runnable engines with rigorous evaluation metrics and a reproducible benchmarking framework.

---

## Algorithmic Engines

### 1. Fair Resource Allocation Engine
- **Greedy Allocation** (implemented in `engine/allocation/greedy.py`): Myopically fulfills highest-priority agency demand first.
- **Fairness-Aware Allocation** (implemented in `engine/allocation/fair.py`): Maximizes Jain's Fairness Index and equalizes fulfillment ratios across agencies.

### 2. Dynamic Volunteer Dispatch Engine
- **Nearest Volunteer Greedy** (implemented in `engine/dispatch/nearest.py`): Online baseline sequentially assigning the closest feasible volunteer.
- **Score-Based Dispatch** (implemented in `engine/dispatch/scored.py`): Multi-criteria utility function balancing pickup distance, deadline urgency, workload equity, and vehicle capacity utilization.
- **Batch Bipartite Matching** (implemented in `engine/dispatch/batch_matching.py`): Global Minimum Weight Bipartite Matching solved via the Hungarian Algorithm (`scipy.optimize.linear_sum_assignment`).

### 3. Simulation & Benchmarking Framework
- **Synthetic Data Generators** (implemented in `simulation/generators/`): Fully deterministic data generation for locations, food donations, recipient agencies, rescue requests, and volunteers accepting random seeds.
- **Experimental Benchmarks** (implemented in `simulation/benchmarks/`): Automated measurement of execution runtime, allocation rates, Jain's fairness index, request assignment rates, total travel distance, and workload variance across configurable problem sizes (10 to 1,000 items).
- **Statistical Aggregation & Plotting** (implemented in `simulation/analysis/`): Computes mean, median, and standard deviation over repeated runs and automatically generates 7 Matplotlib visual plots.

---

## Core Computer Science

- Greedy Algorithms & Online Decision-Making
- Minimum Weight Bipartite Matching (Hungarian Algorithm)
- Fair Resource Allocation & Jain's Fairness Index
- Geographic Haversine Distance Calculation
- Synthetic Data Generation & Controlled Experimental Benchmarking
- Scalability & Empirical Complexity Analysis

---

## Project Structure

```
.
├── engine/
│   ├── allocation/        # Fair Food Resource Allocation Engine
│   │   ├── fair.py
│   │   ├── greedy.py
│   │   └── result.py
│   ├── dispatch/          # Dynamic Volunteer Dispatch Engine
│   │   ├── batch_matching.py
│   │   ├── distance.py
│   │   ├── feasibility.py
│   │   ├── nearest.py
│   │   ├── result.py
│   │   └── scored.py
│   ├── metrics/           # Evaluation Metrics (Fairness & Dispatch)
│   │   ├── dispatch.py
│   │   └── fairness.py
│   └── models/            # Domain Data Models (Pydantic v2)
│       ├── agency.py
│       ├── donation.py
│       ├── location.py
│       ├── rescue_request.py
│       └── volunteer.py
├── simulation/            # Simulation & Benchmarking Suite
│   ├── analysis/          # Aggregation & Matplotlib Plotting
│   │   ├── aggregate.py
│   │   └── plots.py
│   ├── benchmarks/        # Allocation & Dispatch Benchmark Suites
│   │   ├── allocation_benchmark.py
│   │   ├── dispatch_benchmark.py
│   │   └── results.py
│   ├── generators/        # Deterministic Synthetic Data Generators
│   │   ├── allocation_data.py
│   │   ├── dispatch_data.py
│   │   └── locations.py
│   ├── results/           # Benchmark CSV Output & Visual Plots
│   │   └── plots/
│   ├── scenarios/         # Controlled Scenario Builders
│   │   └── scenario.py
│   └── run_benchmarks.py  # Benchmark CLI Entry Point
├── examples/              # Demonstration Scripts
│   ├── allocation_demo.py
│   └── dispatch_demo.py
├── docs/                  # Formal Algorithmic Documentation
│   ├── allocation-algorithms.md
│   ├── dispatch-algorithms.md
│   ├── problem-formulation.md
│   └── simulation-and-benchmarking.md
└── tests/                 # Comprehensive Pytest Suite
```

---

## Quickstart & Verification

Run the complete unit test suite:
```bash
python -m pytest -v
```

Run the Resource Allocation demonstration:
```bash
python examples/allocation_demo.py
```

Run the Dynamic Volunteer Dispatch demonstration:
```bash
python examples/dispatch_demo.py
```

Run the Simulation & Benchmarking Framework:
```bash
# Run quick verification benchmark:
python -m simulation.run_benchmarks --quick

# Run full scalability benchmark suite:
python -m simulation.run_benchmarks
```

---

## License

MIT License
