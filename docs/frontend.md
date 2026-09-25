# FRADMS Frontend Web Platform Architecture

## 1. Overview & Visual Design Language

The **FRADMS Frontend Platform** is an interactive, technical decision-support web interface built with **Next.js 14 App Router**, **TypeScript**, **Tailwind CSS**, and **Recharts**.

### Visual Aesthetics & Experience Design
- **Theme**: Dark obsidian (`#090d16`) and deep slate (`#0f172a`) background with glassmorphic cards (`backdrop-blur-md`).
- **Color Tokens**:
  - **Brand Emerald** (`#10b981`): Sustainable food rescue, fair allocation, and high fulfillment ratios.
  - **Cyan / Teal** (`#06b6d4`): Technical algorithm processing, volunteer dispatch, and matching graph optimization.
  - **Amber / Rose**: Workload warnings, pending request status, and baseline comparisons.
- **Cursor Ring Field**: Interactive particle network canvas on the landing page hero section, generating particle ring attraction to mouse movement.

---

## 2. Navigation & Experience Structure

The application provides two distinct, seamlessly integrated user experiences:

### A. Landing Page (`/`)
- **Navbar**: Brand identity, platform quick-links, and "Enter Platform" CTA.
- **Hero Section**: "Smarter Food Rescue. Fairer Allocation. Dynamic Dispatch." headline with CTAs.
- **Cursor Ring Field**: Interactive client-side canvas embedded in the hero.
- **How It Works**: 4-stage visual pipeline (Donation → Allocation → Matching → Rescue Execution).
- **Algorithms Overview**: Card showcase of Allocation & Dispatch algorithms.
- **Quantitative Metrics**: Grid highlighting Jain Fairness, Allocation Rate, Assignment Rate, Distance, and Workload Variance.

### B. Application Dashboard (`/dashboard/...`)
- **Overview Dashboard (`/dashboard`)**: Operational metrics cards (Total Donations, Agency Demand, Active Volunteers, Pending Requests) backed by PostgreSQL database APIs, with Recharts bar and pie charts.
- **Food Allocation Workspace (`/dashboard/allocation`)**: Interactive workspace executing `/allocation/greedy`, `/allocation/fair`, and `/allocation/compare` algorithms with side-by-side metric cards and fulfillment ratio charts.
- **Volunteer Dispatch Workspace (`/dashboard/dispatch`)**: Workspace running Nearest Volunteer, Score-Based Dispatch, and Hungarian Batch Bipartite Matching (`/dispatch/compare`), displaying travel distance and detailed assignment feasibility tables.
- **Donations Management (`/dashboard/donations`)**: Data table & creation modal connected to `/api/v1/donations`.
- **Agencies Management (`/dashboard/agencies`)**: Data table & creation modal connected to `/api/v1/agencies`.
- **Volunteers Management (`/dashboard/volunteers`)**: Data table & creation modal connected to `/api/v1/volunteers`.
- **Rescue Requests Management (`/dashboard/rescue-requests`)**: Data table with status badges connected to `/api/v1/rescue-requests`.
- **Simulation Workspace (`/dashboard/simulation`)**: Monte Carlo simulation parameters controller connected to `POST /api/v1/simulation/quick`.
- **Experimental Benchmarks (`/dashboard/benchmarks`)**: Visual technical benchmark suite displaying scaling trends across problem sizes (10 to 1,000 entities) for runtime, Jain index, travel distance, and workload variance.
- **System Analytics (`/dashboard/analytics`)**: High-level operational summary cards and tradeoff analysis.
- **Algorithm Explorer (`/dashboard/algorithm-explorer`)**: Educational viva/demo page explaining problem formulations, inputs, core ideas, constraints, objectives, complexity, and metrics for all 5 algorithms.

---

## 3. API Integration Layer (`frontend/lib/api/`)

All backend calls consume FastAPI endpoints using `NEXT_PUBLIC_API_URL` (default: `http://127.0.0.1:8000`).

- `client.ts`: Base fetch wrapper handling headers, errors, and JSON responses.
- `donors.ts`: `/api/v1/donors`
- `donations.ts`: `/api/v1/donations`
- `agencies.ts`: `/api/v1/agencies`
- `volunteers.ts`: `/api/v1/volunteers`
- `rescueRequests.ts`: `/api/v1/rescue-requests`
- `allocation.ts`: `/allocation/greedy`, `/allocation/fair`, `/allocation/compare`
- `dispatch.ts`: `/dispatch/nearest`, `/dispatch/scored`, `/dispatch/batch-matching`, `/dispatch/compare`
- `simulation.ts`: `/api/v1/simulation/quick`
- `health.ts`: `/health`, `/api/v1/database/health`

---

## 4. Running the Frontend

### Prerequisites
Node.js 18+ and npm installed.

### Development Mode
```bash
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in browser.

### Production Build
```bash
cd frontend
npm run build
npm start
```
