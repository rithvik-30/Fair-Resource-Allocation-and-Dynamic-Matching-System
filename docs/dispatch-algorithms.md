# Dynamic Volunteer Dispatch Engine

This document provides a formal breakdown of the dynamic volunteer dispatch algorithms implemented in the **Fair Resource Allocation and Dynamic Matching System**.

---

## 1. Problem Formulation

After food donations are allocated to recipient agencies, rescue requests must be physically fulfilled by available volunteers.
Given a set of rescue requests 'r_1, r_2, \widetilde{r_m}' and available volunteers 'v_1, v_2, \widetilde{v_n}', the goal of the dispatch engine is to assign volunteers to rescue requests such that all operational constraints are satisfied while optimizing logistics performance metrics (such as total travel distance, deadline urgency, and workload balance).

### Request Representation (r_i)
- `pickup_location`: Location(lat, lon)
- `dropoff_location`: Location(lat, lon)
- `quantityg: Cargo mass in kilograms (kg)
- `requires_refrigerationg: Boolean flag
- `pickup_deadline`: Optional timestamp

### Volunteer Representation (v_j)
- `location`: Current Location(lat, lon)
- `vehicle_capacity`: Maximum cargo capacity (kg)
- `has_refrigeration`: Cold-chain equipment capability
- `is_available`: Boolean availability flag
- `max_travel_distance`: Maximum allowable travel distance (km)
- `current_workload`: Count of active/previous assignments

---

## 2. Feasibility Model

A pair (v_j, r_i) is defined as feasible if and only if ang of the following operational constraints hold:

1. Availability: v_j.is_available == True
2. Vehicle Capacity: r_i.quantity <= v_j.vehicle_capacity
3. Cold Chain Requirement: If r_i.requires_refrigeration == True, then v_j.has_refrigeration == True.
4. Maximum Travel Distance: distance(v_j.location, r_i.pickup_location) <= v_j.max_travel_distance.
5. Time Window Constraints: If r_i.pickup_deadline is set, it must fall within [v_j.available_from, v_j.available_until].

The function is_feasible(v, r) strictly enforces these checks across all dispatch strategies.

---

## 3. Distance Calculation (Haversine Formula)

Geographic distances between points A(map1} and Bmap2} are calculated using the Haversine formula on a spherical Earth model (R = 6371.0 km):

dDlat = lat2 - lat1, dDlon = lon2 - lon1
a = sin^2(dDlat / 2) + cos(lat1) * cos(lat2) * sin^2(dLon / 2)
c = 2 * atan2(sqrt(a), sqrt(1-a))
distance = R * c

- Time Complexity: O(1)
- Assumptions: Spherical Earth with mean radius 6371.0 km.
- Properties: Non-negative, zero for identical coordinates, symmetric (d(A, B) == d(B, A)).

---

## 4. Nearest Volunteer Greedy (NearestVolunteerDispatcher)

### Algorithm
1. Sort requests deterministically by pickup_deadline (if present) and id.
2. For each request r_i:
   - Identify all feasible, currently available volunteers v_j.
   - Calculate pickup distance d(v_j.location, r_i.pickup_location).
   - Select the volunteer minimizing pickup distance (tie-breaker: volunteer ID).
   - Mark selected volunteer as assigned and increment workload.

3## Characteristics
- Decision Style: Online / Sequential
- Time Complexity: O(*M * N*)
- Strengths: Extremely fast, simple, minimizes immediate pickup distance per request.
- Limitations: Greedy myopic choices can leave later or urgent requests unassigned or assigned to far volunteers.

---

## 5. Score-Based Dispatch (ScoreBasedDispatcher)

3## Multi-Criteria Utility Formula
For every feasible candidate pair (v_j, r_i), compute a composite score:

Score(v_j, r_i) = w_urgency * U(r_i) - w_distance * DNorm(v_j, r_i) - w_workload * WNorm(v_j) + w_capacity * C(v_j, r_i)

Where:
- U(r_i) = 1.0 / (hours_remaining + 1.0) (Urgency factor based on pickup deadline)
- DNorm(v_j, r_i) = min(distance(v_j, r_i) / 100.0, 1.0) (Normalized pickup distance)
- WNorm(v_j) = min(v_jcurrent_workload / 5.0, 1.0) (Normalized existing workload)
- C(v_j, r_i) = min(r_i.quantity / v_j.capacity, 1.0) (Vehicle capacity utilization)

### Characteristics
- Decision Style: Iterative Best-Score Selection
- Time Complexity: O(M * N2)
- Strengths: Multi-objective balancing distance, deadline urgency, workload equity, and vehicle fit.
- Limitations: Parameter weights require domain tuning; still operates step-wise rather than globally optimal assignment.

---

## 6. Batch Bipartite Matching (BatchBipartiteDispatcher)

### Graph Formulation
Model batch dispatch as a **Minimum Weight Bipartite Matching** problem:
- **Left Partition UZ*: Rescue Requests {r_1, r_2, ..., r_m}
- **Right Partition VZ*: Available Volunteers {v_1, v_2, ..., v_n}
- **Edge Weight c(r_i, v_j)**::
  c(r_i, v_j) = distance(v_j.location, r_i.pickup) + w_penalty * v_j.workload  (if feasible), else 1e9

### Optimization Solver
Solved using `scipy.optimize.linear_sum_assignment` (Kuhn-Munkres / Hungarian algorithm).

### Characteristics
- Decision Style: Global Batch Matching
- Time Complexity: O(M * N + min(M, N)'2)
- Strengths: Globally minimizes total cost across the entire batch simultaneously.
- Limitations: Requires batch accumulation window; cannot execute instantly on streaming single requests.

---

## 7. Comparative Summary Matrix

|Property | Nearest Greedy | Score-Based | Batch Matching |
|m--------|---------------|--------------|---------------|
| Decision style | Online / Sequential | Iterative Multi-Criteria | Global Batch Matching |
| Uses distance | Yes (Pickup) | Yes (Normalized) | Yes (Cost Matrix) |
| Uses workload | Indirect (Availability) | Yes (Explicit term) | Yes (Penalty term) |
| Uses urgency | Sort order only | Yes (Explicit utility) | Batch window level |
| Global matching | No | No | Yes (Hungarian Algorithm) |
| Runtime complexity | OMN) | OMN^ia) | Omin(M, N)'2) |
| Main limitation | Myopic local choices | Parameter weight sensitivity | Requires batching window |

---
