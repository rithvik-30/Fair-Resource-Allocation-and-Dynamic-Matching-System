# Fair Resource Allocation and Dynamic Matching System

An algorithmic decision-support system for fair resource allocation and dynamic task matching, applied to food rescue logistics.

---

## Overview

Food rescue organizations need to make two important computational decisions:

1. **Fair Food Resource Allocation**: Determining how surplus food donations should be distributed among recipient agencies with different needs, storage capacities, priorities, and cold-chain requirements.
2. **Dynamic Volunteer Dispatch**: Assigning incoming rescue tasks to available volunteers while considering geographic distance, vehicle capacity, refrigeration compatibility, deadline urgency, and workload equity.

This repository models these decisions as formal algorithmic problems, providing clean, deterministic, and offline-runnable engines with rigorous evaluation metrics, a reproducible benchmarking framework, and a clean **FastAPI backend layer**.

---

## Architecture & System Components

### 1. Fair Resource Allocation Engine
- **Greedy Allocation** (implemented in `engine/allocation/greedy.py`): Myopically fulfills highest-priority agency demand first.
- **Fairness-Aware Allocation** (implemented in `engine/allocation/fair.py`): Maximizes Jain's Fairness Index and equalizes fulfillment ratios across agencies.

### 2. Dynamic Volunteer Dispatch Engine
- **Nearest Volunteer Greedy** (implemented in `engine/dispatch/nearest.py`): Online baseline sequentially assigning the closest feasible volunteer.
- **Score-Based Dispatch** (implemented in `engine/dispatch/scored.py`): Multi-criteria utility function balancing pickup distance, deadline urgency, workload equity, and vehicle capacity utilization.
- **Batch Bipartite Matching** (implemented in `engine/dispatch/batch_matching.py`): Global Minimum Weight Bipartite Matching solved via the Hungarian Algorithm (`scipy.optimize.linear_sum_assignment`).

### 3. Simulation & Benchmarking Framework
- **Synthetic Data Generators** (implemented in `simulation/generators/`): Fully deterministic data generation for locations, food donations, recipient agencies, rescue requests, and volunteers.
- **Experimental Benchmarks** (implemented in `simulation/benchmarks/`): Automated measurement of execution runtime, allocation rates, Jain's fairness index, request assignment rates, total travel distance, and workload variance.

### 4. FastAPI Backend API Layer
- **REST Endpoints** (implemented in `backend/`): Clean REST API exposing allocation, dispatch, comparison, and simulation endpoints.
- **Interactive Swagger UI**: Accessible at `http://localhost:8000/docs`.

---

## Project Structure

```
.
├── backend/               # FastAPI Backend API Layer
│   ├── api/
│   │   ├── routes/        # Thin REST Route Controllers
│   │   │   ├── allocation.py
│   │   │   ├── dispatch.py
│   │   │   ├── health.py
│   │   │   └── simulation.py
│   │   └── schemas/       # Pydantic v2 API Schemas
│   │       ├── allocation.py
│   │       ├── dispatch.py
│   │       └── simulation.py
│   ├── services/          # Business Logic & Service Layer
│   │   ├── allocation_service.py
│   │   ├── dispatch_service.py
│   │   └── simulation_service.py
│   ├── dependencies.py    # FastAPI Dependency Injection
│   └── main.py            # FastAPI Application & Middleware
├── engine/                # Core Algorithmic Engine (Independent)
│   ├── allocation/
│   ├── dispatch/
│   ├── metrics/
│   └── models/
├── simulation/            # Simulation & Benchmarking Suite
│   ├── analysis/
│   ├── benchmarks/
│   ├── generators/
│   ├── scenarios/
│   └── run_benchmarks.py
├── docs/                  # Algorithmic & API Documentation
│   ├── allocation-algorithms.md
│   ├── backend-api.md
│   ├── dispatch-algorithms.md
│   ├── problem-formulation.md
│   └── simulation-and-benchmarking.md
└── tests/                 # Comprehensive Pytest Suite
```

---

## Quickstart & Verification

Run the complete test suite (unit + simulation + API integration):
```bash
python -m pytest -v
```

Start the FastAPI backend development server:
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
Then visit:
- API Root: `http://127.0.0.1:8000/`
- Health Check: `http://127.0.0.1:8000/health`
- Interactive Swagger Documentation: `http://127.0.0.1:8000/docs`

Run the Simulation & Benchmarking Framework:
```bash
python -m simulation.run_benchmarks --quick
```

---

## License

MIT License
