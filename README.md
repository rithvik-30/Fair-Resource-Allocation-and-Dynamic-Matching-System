# Fair Resource Allocation and Dynamic Matching System

An algorithmic decision-support system for fair resource allocation and dynamic task matching, applied to food rescue logistics.

---

## Overview

Food rescue organizations need to make two important computational decisions:

1. **Fair Food Resource Allocation**: Determining how surplus food donations should be distributed among recipient agencies with different needs, storage capacities, priorities, and cold-chain requirements.
2. **Dynamic Volunteer Dispatch**: Assigning incoming rescue tasks to available volunteers while considering geographic distance, vehicle capacity, refrigeration compatibility, deadline urgency, and workload equity.

This repository models these decisions as formal algorithmic problems, providing clean, deterministic, and offline-runnable engines with rigorous evaluation metrics.

---

## Algorithmic Engines

### 1. Fair Resource Allocation Engine
- **Greedy Allocation** (implemented in engine/allocation/greedy.py): Myopically fulfills highest-priority agency demand first.
- **Fairness-Aware Allocation** (implemented in engine/allocation/fair.py): Maximizes Jain's Fairness Index and equalizes fulfillment ratios across agencies.

### 2. Dynamic Volunteer Dispatch Engine
- **Nearest Volunteer Greedy** (implemented in engine/dispatch/nearest.py): Online baseline sequentially assigning the closest feasible volunteer.
- **Score-Based Dispatch** (implemented in engine/dispatch/scored.py): Multi-criteria utility function balancing pickup distance, deadline urgency, workload equity, and vehicle capacity utilization.
- **Batch Bipartite Matching** (implemented in engine/dispatch/batch_matching.py): Global Minimum Weight Bipartite Matching solved via the Hungarian Algorithm (scipy.optimize.linear_sum_assignment).

---

## Core Computer Science

- Greedy Algorithms & Online Decision-Making
- Minimum Weight Bipartite Matching (Hungarian Algorithm)
- Fair Resource Allocation & Jain's Fairness Index
- Geographic Haversine Distance Calculation
- Complexity & Scalability Analysis

---

## Project Structure

`	ext
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
├── examples/              # Demonstration Scripts
│   ├── allocation_demo.py
│   └── dispatch_demo.py
├── docs/                  # Formal Algorithmic Documentation
│   ├── allocation-algorithms.md
│   ├── dispatch-algorithms.md
│   └── problem-formulation.md
└── tests/                 # Comprehensive Pytest Suite
`

---

## Quickstart & Verification

Run the complete unit test suite:
`ash
python -m pytest -v
`

Run the Resource Allocation demonstration:
`ash
python examples/allocation_demo.py
`

Run the Dynamic Volunteer Dispatch demonstration:
`ash
python examples/dispatch_demo.py
`

---

## License

MIT License
