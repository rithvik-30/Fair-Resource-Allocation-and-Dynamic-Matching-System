# PostgreSQL + SQLAlchemy Persistence Architecture

## 1. Overview & Technology Selection

The **Fair Resource Allocation & Dynamic Matching System** uses **PostgreSQL** with **SQLAlchemy 2.x** and **Alembic** for persistence.

### Key Architectural Rule: Algorithmic Engine Isolation
The core decision engine under engine/ is strictly independent of the database and FastAPI. Algorithmic engines operate on pure domain models (Donation, Agency, Volunteer, RescueRequest) and return pure evaluation result dataclasses. The database and repository layers act purely as a persistence adapter around the application.

### Tech Stack
- **Database**: PostgreSQL (relational model for structured domain entities and execution logs)
- **ORM**: SQLAlchemy 2.x with typed declarative mappings
- **Migrations**: Alembic for schema migrations
- **Driver**: psycopg 3 (postgresql+psycopg://)

---

## 2. Architecture Diagram

`
                 +-----------------------+
                 |    HTTP Requests      |
                 | (FastAPI API Layer)   |
                 +-----------+-----------+
                             |
                             v
                 +-----------------------+
                 |    Service Layer      |
                 | (Orchestration & DB)  |
                 +-----+-----------+-----+
                       |           |
                       v           v
+------------------------+      +-------------------------+
|    Algorithmic Engine  |      |   Persistence Adapter   |
| (Allocation & Dispatch)|      |   (Repository & Models) |
+------------------------+      +------------+------------+
                                             |
                                             v
                                +-------------------------+
                                |  PostgreSQL Database    |
                                +-------------------------+
`

---

## 3. Database Schema & Entities

### Core Tables

1. **donors**: Stores food donor profiles (name, coordinates).
2. **donations**: Food items available for allocation linked to a donor.
3. **gencies**: Recipient agencies with food demand, storage capacity, priority, and refrigeration requirements.
4. **olunteers**: Available rescue volunteers with capacity, availability windows, vehicle specs, and workload.
5. **
escue_requests**: Open rescue tasks matching a donation with an agency.
6. **llocation_records**: Persisted outcomes of resource allocation runs.
7. **dispatch_records**: Persisted outcomes of volunteer dispatch operations.

### Entity Relationships

`
Donor (1) ----< (N) Donation (1) ----< (N) RescueRequest (N) >---- (1) Agency
                      |                                               |
                      v                                               v
               AllocationRecord                                AllocationRecord

Volunteer (1) ----< (N) DispatchRecord
`

---

## 4. Repository & Service Layer

The database operations follow a clean repository pattern in ackend/db/repositories/:
- DonorRepository
- DonationRepository
- AgencyRepository
- VolunteerRepository
- RescueRequestRepository
- AllocationRecordRepository
- DispatchRecordRepository

Services (ackend/services/) query entities from repositories, construct engine domain models, execute allocation/dispatch algorithms, and write resulting AllocationRecord or DispatchRecord entities back to PostgreSQL.

---

## 5. Configuration & Setup

### Environment Variables
Configure DATABASE_URL in a .env file (copied from .env.example):
`env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/fradms
`

### Running Alembic Migrations
`ash
# Apply migrations to head
alembic upgrade head

# Rollback single migration
alembic downgrade -1
`

### Seeding Development Data
`ash
python scripts/seed_database.py
`

### Running the API & Verifying Health
`ash
uvicorn backend.main:app --reload

# Health verification
curl http://localhost:8000/api/v1/database/health
`
