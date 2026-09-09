# Fair Resource Allocation and Dynamic Matching System

An algorithmic decision-support system for fair resource allocation and dynamic task matching, applied to food rescue logistics.

## Overview

Food rescue organizations need to make two important decisions:

1. **Resource Allocation** — deciding how surplus food should be distributed among recipient agencies with different needs, capacities, priorities, and locations.
2. **Dynamic Matching** — assigning incoming rescue requests to available volunteers while considering distance, vehicle capacity, urgency, availability, and workload.

This project models these decisions as computational problems and compares different algorithmic approaches through simulation and benchmarking.

The goal is not simply to build a food-rescue application, but to study how different algorithms perform when solving resource allocation and dynamic matching problems.

---

## Core Computer Science

The project focuses on:

- Greedy algorithms
- Bipartite matching
- Fair resource allocation
- Integer Linear Programming (ILP)
- Dynamic / online decision-making
- Graph-based modelling
- Simulation
- Algorithm benchmarking
- Complexity and scalability analysis

---

## Algorithmic Approach

### 1. Food Allocation

Determine how available food should be distributed among recipient agencies.

Planned approaches:

- Greedy allocation
- Fairness-aware allocation
- Integer Linear Programming optimization

### 2. Volunteer Dispatch

Determine which available volunteer should handle each rescue request.

Planned approaches:

- Nearest-volunteer greedy matching
- Score-based matching
- Batch bipartite matching

The approaches will be evaluated against common scenarios rather than assuming that one algorithm is always optimal.

---

## Simulation and Benchmarking

A simulation environment will generate different combinations of:

- Donors
- Recipient agencies
- Volunteers
- Food donations
- Rescue requests
- Availability windows
- Geographic locations

The algorithms will be compared using metrics such as:

- Food successfully allocated
- Travel distance
- Response time
- Resource utilization
- Allocation fairness
- Volunteer workload fairness
- Execution time
- Scalability

Experiments will investigate questions such as:

- How does fairness affect efficiency?
- When does global matching outperform greedy approaches?
- How do the algorithms behave as the number of requests and volunteers increases?
- What trade-offs exist between solution quality and computational cost?

---

## System Architecture

```text
                    Input Data
                        │
                        ▼
                Simulation Engine
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      Allocation Engine      Dispatch Engine
             │                     │
       ┌─────┼─────┐         ┌─────┼─────┐
       │     │     │         │     │     │
    Greedy Fair   ILP     Nearest Score  Batch
       │     │     │         │     │     │
       └─────┴─────┘         └─────┴─────┘
             │                     │
             └──────────┬──────────┘
                        ▼
                  Metrics Engine
                        │
                        ▼
                   Benchmarking
                        │
                        ▼
                  FastAPI Backend
                        │
                        ▼
               PostgreSQL / PostGIS
                        │
                        ▼
                Next.js Dashboard

Tech Stack
Algorithm Engine
Python
NetworkX
Google OR-Tools
NumPy
Pytest
Simulation & Evaluation
Pandas
Matplotlib
Backend
FastAPI
Pydantic
Database
PostgreSQL
PostGIS
Frontend
Next.js
TypeScript
Tailwind CSS
Leaflet
Recharts
Infrastructure
Docker
GitHub Actions
Development Philosophy

The project follows an algorithm-first approach.

The allocation, matching, and optimization algorithms will be developed and tested independently before being integrated into the backend and frontend.

Each algorithm will be evaluated not only on whether it produces a valid solution, but also on:

Solution quality
Fairness
Efficiency
Runtime
Scalability

This allows the project to serve as both a practical system and an experimental platform for comparing algorithmic approaches.

Project Status

🚧 Under Development

Current focus:

Project architecture
Problem formulation
Algorithm design
Simulation environment
License

MIT License