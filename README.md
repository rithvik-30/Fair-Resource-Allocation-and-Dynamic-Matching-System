# Fair Resource Allocation and Dynamic Matching System

An algorithmic decision-support system for fair resource allocation and dynamic task matching, applied to food rescue logistics.

---

## Overview

Food rescue organizations need to make two important computational decisions:

1. **Fair Food Resource Allocation**: Determining how surplus food donations should be distributed among recipient agencies with different needs, storage capacities, priorities, and cold-chain requirements.
2. **Dynamic Volunteer Dispatch**: Assigning incoming rescue tasks to available volunteers while considering geographic distance, vehicle capacity, refrigeration compatibility, deadline urgency, and workload equity.

This repository models these decisions as formal algorithmic problems, providing clean, deterministic, and offline-runnable engines with rigorous evaluation metrics, a reproducible benchmarking framework, a clean **FastAPI backend layer**, and **PostgreSQL + SQLAlchemy persistence**.

---

## Architecture & System Components

### 1. Fair Resource Allocation Engine
- **Greedy Allocation** (implemented in engine/allocation/greedy.py): Myopically fulfills highest-priority agency demand first.
- **Fairness-Aware Allocation** (implemented in engine/allocation/fair.py): Maximizes Jain's Fairness Index and equalizes fulfillment ratios across agencies.

### 2. Dynamic Volunteer Dispatch Engine
- **Nearest Volunteer Greedy** (implemented in engine/dispatch/nearest.py): Online baseline sequentially assigning the closest feasible volunteer.
- **Score-Based Dispatch** (implemented in engine/dispatch/scored.py): Multi-criteria utility function balancing pickup distance, deadline urgency, workload equity, and vehicle capacity utilization.
- **Batch Bipartite Matching** (implemented in engine/dispatch/batch_matching.py): Global Minimum Weight Bipartite Matching solved via the Hungarian Algorithm (scipy.optimize.linear_sum_assignment).

### 3. Simulation & Benchmarking Framework
- **Synthetic Data Generators** (implemented in simulation/generators/): Fully deterministic data generation for locations, food donations, recipient agencies, rescue requests, and volunteers.
- **Experimental Benchmarks** (implemented in simulation/benchmarks/): Automated measurement of execution runtime, allocation rates, Jain's fairness index, request assignment rates, total travel distance, and workload variance.

### 4. FastAPI Backend API Layer
- **REST Endpoints** (implemented in ackend/): Clean REST API exposing allocation, dispatch, database CRUD, and simulation endpoints.
- **Interactive Swagger UI**: Accessible at http://localhost:8000/docs.

### 5. PostgreSQL + SQLAlchemy Persistence Layer
- **Database Engine**: PostgreSQL with SQLAlchemy 2.x typed ORM mappings and psycopg 3.
- **Database Migrations**: Alembic reproducible database schema migrations.
- **Repositories**: Isolated data-access layer under ackend/db/repositories/.
- **Engine Boundary Isolation**: The core algorithmic engine (engine/) remains 100% independent of SQLAlchemy and PostgreSQL.

---

## Project Structure

`
.
├── backend/               # FastAPI Backend & Database Layer
│   ├── api/
│   │   ├── routes/        # REST Controllers (allocation, dispatch, database, health, simulation)
│   │   └── schemas/       # Pydantic v2 API Schemas
│   ├── db/                # Database Configuration & Repositories
│   │   ├── repositories/  # Repository Layer for Donors, Donations, Agencies, Volunteers, Requests
│   │   ├── base.py        # SQLAlchemy Base
│   │   ├── models.py      # SQLAlchemy 2.x ORM Entities
│   │   └── session.py     # Engine & Session Management
│   ├── services/          # Service Layer Orchestration
│   ├── dependencies.py    # FastAPI DB Session & Dependency Injection
│   └── main.py            # FastAPI Entry Point
├── engine/                # Core Algorithmic Engine (Independent)
├── simulation/            # Simulation & Benchmarking Suite
├── alembic/               # Database Migrations
├── docs/                  # System Documentation (database.md, backend-api.md, etc.)
├── scripts/               # Utility Scripts (seed_database.py)
└── tests/                 # Pytest Suite (Domain, Engine, API, DB)
`

---

## Quickstart & Database Commands

### 1. Database Setup & Migrations
Configure DATABASE_URL in .env:
`env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/fradms
`
Apply Alembic migrations:
`ash
alembic upgrade head
`

Seed initial dataset:
`ash
python scripts/seed_database.py
`

### 2. Running Tests
Run the complete test suite (includes in-memory DB tests):
`ash
python -m pytest -v
`

### 3. Running the FastAPI Backend Server
`ash
python -m uvicorn backend.main:app --reload --port 8000
`
Then visit:
- Health Check: http://127.0.0.1:8000/health
- Database Health Check: http://127.0.0.1:8000/api/v1/database/health
- Interactive Swagger Documentation: http://127.0.0.1:8000/docs

---

## License

MIT License
