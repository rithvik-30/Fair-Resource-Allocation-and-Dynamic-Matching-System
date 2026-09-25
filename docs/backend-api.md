# FastAPI Backend API Documentation

## 1. Architecture Overview

The backend is built using **FastAPI** and acts as an adapter layer connecting external clients (such as a future Next.js frontend) with the underlying algorithmic engines and simulation suite.

```
Future Next.js Frontend (http://localhost:3000)
             │  (HTTP / REST JSON)
             ▼
      FastAPI API Routes (backend/api/routes/)
             │  (Pydantic v2 Validation & Schemas)
             ▼
      Service Layer (backend/services/)
             │  (Orchestration & Copy Isolation)
             ▼
   Algorithmic Engine & Simulation (engine/ & simulation/)
     ├── Fair Food Allocation Engine
     ├── Dynamic Volunteer Dispatch Engine
     └── Synthetic Simulation Framework
```

### Architectural Principles
1. **Engine Independence**: The core algorithmic code inside `engine/` remains completely independent of web frameworks.
2. **Thin Route Controllers**: API route handlers only perform parameter validation and delegate execution to the service layer.
3. **Stateless Service Layer**: Services receive request payloads, deep-copy inputs to prevent mutation, execute the engine algorithms, and format structured responses.

---

## 2. API Endpoints Reference

Base URL: `http://localhost:8000`

### Health & Info Endpoints
- `GET /health`: Service health check (`{"status": "ok", "service": "FRADMS API"}`).
- `GET /`: Service metadata, version, and links to documentation.

### Fair Food Resource Allocation (`/api/v1/allocation`)
- `POST /api/v1/allocation/greedy`: Fulfills highest-priority agency demand myopically.
- `POST /api/v1/allocation/fair`: Maximizes Jain's Fairness Index and equalizes fulfillment ratios.
- `POST /api/v1/allocation/compare`: Runs both greedy and fairness-aware algorithms on the input scenario and returns side-by-side comparative metrics.

### Dynamic Volunteer Dispatch (`/api/v1/dispatch`)
- `POST /api/v1/dispatch/nearest`: Online greedy baseline matching closest feasible volunteer.
- `POST /api/v1/dispatch/scored`: Multi-criteria utility function balancing distance, deadline urgency, workload equity, and vehicle capacity.
- `POST /api/v1/dispatch/batch`: Global Minimum Weight Bipartite Matching solved via Hungarian algorithm.
- `POST /api/v1/dispatch/compare`: Runs all three dispatch strategies on the same request set and returns structured comparative metrics.

### Simulation & Benchmarking (`/api/v1/simulation`)
- `POST /api/v1/simulation/quick`: Executes a lightweight benchmark (`sizes: [10, 25, 50]`, `seed: 42`), returning aggregated metrics and list of generated Matplotlib plot filenames.

---

## 3. Running the Server

Start the FastAPI development server with auto-reload:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Access Interactive Documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 4. Development CORS

For local development, CORS is configured in `backend/main.py` to allow cross-origin requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

---

## 5. Testing & Verification

Run the full Pytest test suite (unit + simulation + API integration):

```bash
python -m pytest -v
```
