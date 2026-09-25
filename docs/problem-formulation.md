# Problem Formulation: Fair Resource Allocation & Dynamic Volunteer Dispatch

## 1. Executive Summary & Problem Overview

The **Fair Resource Allocation and Dynamic Matching System** addresses the critical operational challenges faced by food rescue organizations. Every day, large quantities of perishable food are donated by commercial donors (supermarkets, restaurants, farms), while recipient agencies (food banks, shelters, community centers) experience varying degrees of food insecurity. 

Connecting these entities efficiently and equitably requires solving two distinct, interconnected computational problems:

1. **Fair Food Resource Allocation** Deciding *how much* food from available donations to assign to which recipient agencies, subject to capacity limits, urgency, demand, priority, and historical allocation fairness.
2. **Dynamic Volunteer Dispatch**: Deciding *which volunteer* should transport each allocated rescue task from pickup to dropoff, accounting for geographical locations, vehicle capacity, time windows, and volunteer workload balance.

This document formalizes the mathematical models, entities, constraints, objective functions, and operational assumptions underlying both computational problems.

---

## 2. Distinction Between Allocation and Dispatch

It is fundamental to decouple **Resource Allocation** from **Volunteer Dispatch**:

| Dimension | Resource Allocation | Volunteer Dispatch |
| :-- | :-- | :-- |
| **Primary Question** | *Who gets what food, and in what quantities?* | *Who transports the food from donor to recipient?* |
| **Primary Decision Variables** | Continuous / Integer allocation quantities $x_{j,i}$ (kg) | Binary assignment variables $y_{r,v} \en \{0, 1}\}$ |
| **Key Objectives** | Maximize total food allocated, minimize wastage, maximize priority-weighted demand satisfaction, enforce historical/envy-aware fairness | Minimize total travel distance, minimize response time, balance volunteer workload, maximize task completion |
| **Primary Constraints** | Donor supply, Agency storage capacity, Agency demand, Cold chain compatibility | Vehicle weight/volume capacity, Volunteer availability window, Refrigeration capability, Route length limits |
| **Execution Timing** | Batch / Periodic (e.g., when new donations are posted) | Dynamic / Real-time / Sliding window |
| **Output Entity** | `AllocationResult` (giving rise to a `RescueRequest`) | `Match` (assigning a `RescueRequest` to a `Volunteer`) |

By separating these decisions, the system prevents combinatorial explosion and allows specialized optimization algorithms (e.g., Fair Allocation heuristics / ILP for distribution, and Bipartite Matching / VRP for logistics).

---

## 3. Core Domain Entities & Attributes

The system relies on six primary domain entities:

### 3.1. Donor
Represents a source of surplus food (e.g., grocery store, cafeteria, farm).
- `id`(`str`): Unique identifier.
- `name`(`str`): Entity name.
- `location` (`Location`): Geo-coordinates `(latitude, longitude)`.
- `operating_hours` (`Tuple[str, str]`): Operational window `(start_time, end_time)` in HH:MM format.
- `contact_info` (`Optional[str]`): Contact details.

### 3.2. Agency (Recipient)
Represents a beneficiary organization (e.g., shelter, soup kitchen, food bank).
- `id`(`str`): Unique identifier.
- `name`(`str`): Organization name.
- `location` (`Location`): Geo-coordinates `(latitude, longitude)`.
- `storage_capacity` (`float`): Maximum storage volume/weight (kg).
- `current_inventory` (`float`): Current food inventory in storage (kg).
- `demands` (`float`): Current food demand/need (kg).
- `priority_score`(`float`): Priority weight $w_i \en [1.0, 10.0]$ reflecting vulnerability or population served.
- `historical_allocations` (`float`): Total cumulative food received over recent evaluation window (kg).
- `refrigeration_capable` (`bool`): True if cold storage is available.

### 3.3. Donation
Represents a batch of surplus food offered by a donor.
- `id` (`str`): Unique identifier.
- `donor_id`(`str`): Reference to Donor `id`,
- `food_type` (`str`): Food category (e.g., "perishable_produce", "prepared_meals", "non_perishable").
- `quantity` (`float`): Offered quantity (kg).
- `perishable`(`bool`): Indicates rapid degradation risk.
- `expiration_hours` (`Optional[float]_`): Time window (hours) until food spoils.
- `requires_refrigeration` (`bool`): True if cold chain transport/storage is required.
- `created_at` (`datetime`): Timestamp of donation creation.
- `location` (`Optional[Location]_`): Pickup location (defaults to Donor location).

### 3.4. Volunteer
Represents a volunteer driver available to perform pickups and deliveries.
- `id`(`str`): Unique identifier.
- `name`(`str`): Volunteer name.
- `location` (`Location`): Current location coordinates `(latitude, longitude)`.
- `vehicle_capacity`(`float`): Maximum weight capacity (kg).
- `has_refrigeration` (`bool`): True if vehicle supports cold transport.
- `available_from`(`Optional[datetime]`): Start of availability window.
- `available_until` (`Optional[datetime]_`): End of availability window.
- `max_travel_distance`(`Optional[float]`): Maximum allowed travel distance (km).
- `current_workload` (`int`): Count of currently active assignments.
- `total_distance_traveled` (`float`): Cumulative distance traveled (km).
- `is_available` (`bool`): Operational status toggle.

### 3.5. RescueRequest
Represents a physical transportation task generated after food allocation.
- `id` (`str`): Unique identifier.
- `donation_id`(`str`): Reference to associated Donation.
- `agency_id` (`str`): Reference to target Agency.
- `pickup_location` (`Location`): Donor pickup coordinates.
- `dropoff_location`(`Location`): Agency dropoff coordinates.
- `quantity`(`float`): Quantity to transport (kg).
- `requires_refrigeration` (`bool`): Cold chain requirement.
- `pickup_deadline` (`Optional[datetime]`): Expiration / pickup deadline.
- `dropoff_deadline` (`Optional[datetime]`): Agency receipt deadline.
- `status` (`RequestStatus`): Task state (`PENDING`, `ASSIGNED`, `IN_TRANSIT`, `COMPLETED`, `CANCELLED`).

### 3.6. Match
Represents the assignment of a `RescueRequest` to a `Volunteer`.
- `id` (`str`): Unique identifier.
- `request_id`(`str`): Reference to RescueRequest.
- `volunteer_id` (`str`): Reference to Volunteer.
- `assigned_at`(`datetime`): Assignment timestamp.
- `estimated_distance` (`float`): Estimated travel distance (km).
- `status` (`MatchStatus`): State (`ASSIGNED`, `PICKED_UP`, `COMPLETED`, `FAILED`).

---

## 4. Problem 1 Formulation: Fair Food Resource Allocation

### 4.1. Inputs
- Set of available donations $\mathcal{D} = \{1, \dots, m\}$, where donation $jd has quantity $S_j$, refrigeration requirement $R_j^{req} \in \{0, 1\}$, and location $L_j^D$.
- Set of recipient agencies $\mathcal{A} = \{1, \dots, n\}$, where agency $i$ has demand $D_i$, remaining storage capacity $C_i^{rem} = \max(0, \text{storage__capacity}_i - \text{current__inventory}_i)$, priority weight $w_i \ge 1$, historical allocation $H_i$,
  refrigeration capability $R_I^{cap} \in \{0, 1\}$, and location $L_i^A$.

### 4.2. Decision Variables
- $x_{j,i} \ge 0$: Quantity (in kg) of donation $j$ allocated to agency $i$.

### 4.3. Hard Constraints
1. **Supply Bounds**:
   $$\sum_{i \in \mathcal{A}} x_{j,i} \le S_j \quad \forall j \in \mathcal{D}$$
   *No donation can be allocated beyond its available quantity.*

2. **Demand Bounds**:
   $$\sum_{j \in \mathcal{D}} x_{j,i} \le D_i \quad \forall i \in \mathcal{A}$$
   *No agency receives more food than its requested demand.*

3. **Storage Capacity Bounds**:
   $$\sum_{j \in \mathcal{D}} x_{j,i} \le C_i^{rem} \quad \forall i \in \mathcal{A}$$
   *Allocated food must not exceed physical storage space.*

4. **Cold Chain Compatibility**:
   $$x_{j,®("u.j^{req} \cdot (1 - R_i^{cap}) = 0 \quad \forall j \in \mathcal{D}, \forall i \in \mathcal{A}$$
   *Refrigerated donations can only be allocated to refrigeration-capable agencies.*

5. **Non-negativity**:
   $$x_{j, i} \ge 0 \quad \forall² \in \mathcal{D}, \forall i \in \mathcal{A}$$

### 4.4. Objective Functions

Different allocation algorithms optimize different combinations of efficiency and equity:

1. **Efficiency Maximization (Greedy Baseline)**:
   $$\max \sum_{j \in \mathcal{D}} \sum_{i \in \mathcal{A}} x_{j,i}$$
:2. **Priority-Weighted Efficiency**:
   $$\max \sum_{j \in \mathcal{D}} \sum_{i \in \mathcal{A}} w_i \cdot x_{j, i}$$

3. **Fairness-Aware Allocation**:
   Let the total allocation ratio for agency $i$ be $r_i = \frac{H_1 + \sum_{j} x_{j, i}}{D_i}$.
   Fairness objectives penalize variance or equalize satisfaction ratios:
   - **Max-Min Bottleneck Fairness**: $<max \min_{i \in \mathcal{A}} r_i$
    - **Jain's Fairness Index Maximization**: 
     $$\mathcal{J}(r) = \frac{\left( \sum_{i=1}nn r_i \right)^2};n \sum_{i=1}nn r_i^2}$$
   - **Alpha-Fairness Objective** (for parameter $\alpha \ge 0$):
     $$\max \sum_{i \in \mathcal{A}} w_i \frac{r_i^{1-\alpha}}{1{\alpha}}$$

---

## 5. Problem 2 Formulation: Dynamic Volunteer Dispatch

### 5.1. Inputs
- Set of active rescue requests $\mathcal{R} = \{1, \dots, K\}$, each request $r$ having pickup location $L_r^P$, dropoff location $L_r^D$, weight $q_r$, refrigeration flag $R_r^{req}$, and time window [T_r^{start}, T_r^{end}]$.
- Set of candidate volunteers $\mathcal{V} = \{1, \dots, V\}$, each volunteer $v$ having current position $L_v^V$, vehicle capacity $W_v$, refrigeration support $R_v^{cap}$, current workload $U_vd, and maximum travel distance limit $M_v)$.

### 5.2. Decision Variables
- $y_{r,v} \in \{0, 1\}$: Binary variable equal to 1 if volunteer $v$ is assigned to rescue request $r$, and 0 otherwise.

### 5.3. Hard Constraints
1. **Single Assignment Per Request**:
   $$\sum_{v \in \mathcal{V}} y_{r,v} \le 1 \quad \forall r \in \mathcal{R}$$
   *Each request is assigned to at most one volunteer.*

2. **Vehicle Capacity Limit**:
   $$q_r \cdot y_{r,v} \le W_v \quad \forall r \in \mathcal{R}, \forall v \in \mathcal{V}$$
   *Volunteer vehicle capacity must accommodate request weight.*

3. **Cold Chain Requirement**:
   $$y_{r,v} \cdot R_r^{req} \cdot (1 - R_v^{cap}) = 0 \quad \forall r \in \mathcal{R}, \forall v \in \mathcal{V}$$
   *Refrigerated requests require refrigeration-capable vehicles.*

4. **Distance / Workload Bounds**:
   $$\text{dist}(L_v^V, L_r^P) + \text{dist}(L_r^P, L_r^D) \le M_v \quad \text{if } y_{r,v} = 1$$
   *Total route distance must not exceed volunteer maximum distance.*

5. **Volunteer Workload Cap**:
   $$\sum_{r \in \mathcal{R}} y_{r,v} + U_v \le \frac{MAxTasks}_v \quad \forall v \in \mathcal{V}$$

### 5.4. Objective Functions
1. **Nearest Volunteer (Greedy)**:
   $$\min \sum_{r \in \mathcal{R}} \sum_{v \in \mathcal{V}} y_{r,v} \cdot \text{dist}(L_v^V, L_r^P)$$

2. **Total Logistics Cost Minimization (Global Distance)**:
   $$\min \sum_{r \in \mathcal{R}} \sum_{v \F–âÆÖF†6Çµg×Ò•÷·"ÇgÒÆ6F÷BÄ&–r‚ÇFW‡G¶F—7GÒ„Å÷eåbÂÅ÷%å’²ÇFW‡G¶F—7GÒ„Å÷%åÂÅ÷%äB’Ä&–r’B@ £2â¢¤×VÇF’Ôö&¦V7F—fR&—'F—FRÖF6†–ær66÷&R¢£ ¢BEÆÖ‚Ç7VÕ÷·"Æ–âÆÖF†6Çµ'×ÒÇ7VÕ÷·bÆ–âÆÖF†6Çµg×Ò•÷·"ÇgÒÆ6F÷BÇFW‡Gµ66÷&WÒ‡"Âb’B@¢v†W&REÇFW‡Gµ66÷&WÒ‡"Âb’ÒÆÇ†óÆ6F÷BÇFW‡GµW&vVæ7—Ò‡"’ÒÆÇ†ó"Æ6F÷BÇFW‡G´F—7Fæ6WÒ‡"Âb’ÒÆÇ†ó2Æ6F÷BÇFW‡Gµv÷&¶ÆöGÒ‡b’Bà ¢ÒÒÐ ¢22bâ÷W&F–öæÂ77V×F–öç2bÖF†VÖF–6Â&÷VæG0 £â¢¤WV6Æ–FVâòw&VBÔ6—&6ÆRF—7Fæ6R¢£¢F—7Fæ6W2&RÖöFVÆVBW6–ær†fW'6–æRf÷&×VÆ2öâvVöw&†–6Â6ö÷&F–æFW2†ÆBÂÆöâ’2FWFW&Ö–æ—7F–2ÖWG&–2&÷‡’ã£"â¢¤F—f—6–&–Æ—G’öb7W'ÇW2¢£¢–âfööBÆÆö6F–öâÂ—FV×26â&RF—f–FVB–çFò6öçF–çV÷W2vV–v‡BVæ—G2†¶r’ã£2â¢¤–æf÷&ÖF–öâ–çFVw&—G’¢£¢VçF—F–W2G'WF†gVÆÇ’&W÷'B66—F–W2ÂFVÖæG2ÂæBf–Æ&–Æ—G’v–æF÷w2ã£Bâ¢¤–æFWVæFVçBW†V7WF–öâ†6W2¢£¢ÆÆö6F–öâ—26ö×WFVBW"&F6‚öbFöæF–öç3²&W7VÇF–ærÆÆö6F–öç27vâ&W67VR&WVW7G2v†–6‚&RF—7F6†VB–â&VÂ×F–ÖR÷"&F6‚v–æF÷w2à ¢ÒÒÐ ¢22râÖWG&–72f÷"Æv÷&—F†Ö–2&Væ6†Ö&¶–æp ¤Æv÷&—F†×27&÷72&÷F‚†6W2v–ÆÂ&R•ÖÇVFVBöâ7FæF&F—¦VBVçF—FF—fRÖWG&–73  £â¢¤fööBÆÆö6F–öâ&FR¢£¢EÇFW‡GµF÷FÂVçF—G’ÆÆö6FVGÒòÇFW‡GµF÷FÂFöæF–öâ7WÇ—Ò@£"â¢¤FVÖæB6F—6f7F–öâ&FR¢£¢EÇFW‡GµF÷FÂVçF—G’&V6V—fVB'’vVæ6–W7ÒòÇFW‡GµF÷FÂvVæ7’FVÖæGÒ@£2â¢¤¦–âw2f—&æW72–æFW‚…ÆÖF†6Ç´§Ò’¢£¢FVw&VRöbÆÆö6F–öâWVÆ—G’7&÷72&V6—–VçBvVæ6–W2‚CÆÆRÆÖF†6Ç´§ÒÆÆRB’ã£Bâ¢¥v÷&¶ÆöBf&–æ6R¢£¢7FæF&BFWf–F–öâöbF—7Fæ6W2÷F6·276–væVBFò7F—fRföÇVçFVW'2ã£Râ¢¥F÷FÂbfW&vRF—7Fæ6R¢£¢Æöv—7F–72Ö–ÆVvR–æ7W'&VBW"&W67VVB¶–Æöw&Òã£bâ¢¤W†V7WF–öâ'VçF–ÖRb66Æ&–Æ—G’¢£¢6ö×WFF–öæÂÆFVæ7’†×2’2&ö&ÆVÒ66ÆRDâÆ–â³ÂÒBw&÷w2à 