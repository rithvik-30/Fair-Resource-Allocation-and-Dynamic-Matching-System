# Food Resource Allocation Algorithms & Fairness Metrics

This document details the mathematical formulations, decision workflows, complexity bounds, and comparative trade-offs for the resource allocation engine of the **Fair Resource Allocation & Dynamic Matching System**.

---

## 1. Problem Formulation

Given a set of incoming food donations $\\mathcal{D} = \\{d_1, d_2, \\dots, d_m\\}$ and recipient agencies $\\mathcal{A} = \\{a_1, a_2, \\dots, a_n\\}$, the goal is to determine an allocation quantity {i,j} \\ge 0$ representing food assigned from donation $ to agency $.

### Core Constraints:
1. **Supply Constraint:** For every donation $, $\\sum_{j=1}^n x_{i,j} \\le \\text{quantity}(d_i)$.
2. **Demand Constraint:** For every agency $, $\\sum_{i=1}^m x_{i,j} \\le \\text{demands}(a_j)$.
3. **Storage Capacity Constraint:** For every agency $, $\\sum_{i=1}^m x_{i,j} \\le \\text{storage\\_capacity}(a_j) - \\text{current\\_inventory}(a_j)$.
4. **Refrigeration Compatibility:** If donation $ requires refrigeration ($\\text{requires\\_refrigeration}(d_i) = \\text{True}$), then {i,j} > 0 \\implies \\text{refrigeration\\_capable}(a_j) = \\text{True}$.

---

## 2. Greedy Allocation Baseline

### Objective
Maximized rapid throughput by allocating donation supply to eligible agencies based on expiration urgency and priority score.

### Decision Workflow
1. Sort donations $\\mathcal{D}$ by perishability and expiration time.
2. For each donation $, filter eligible agencies $\\mathcal{A}_{\\text{eligible}} \\subseteq \\mathcal{A}$ respecting demand, storage, and cold-chain constraints.
3. Sort eligible agencies by priority_score (descending).
4. Fulfill remaining demand of the top-priority agency before proceeding to subsequent agencies.

### Complexity Analysis
- **Time Complexity:** (M \\cdot N \\log N)$, where  = |\\mathcal{D}|$ and  = |\\mathcal{A}|$.
- **Space Complexity:** (M + N)$ for state tracking.

### Strengths & Limitations
- **Strengths:** Simple implementation, minimal runtime overhead, guarantees priority fulfillment.
- **Limitations:** Suffers from starvation for low-priority agencies when supply is scarce.

---

## 3. Fairness-Aware Allocation

### Objective
Reduce allocation disparity across recipient agencies by equalizing satisfaction ratios.

### Allocation Ratio Definition
\\text{allocation\\_ratio}_j = \\frac{\\text{historical\\_allocation}_j + \\text{new\\_allocation}_j}{\\text{demand}_j}

### Max-Min Water-Filling Algorithm
Rather than filling an agency completely, the fairness-aware allocator equalizes the priority-weighted allocation ratio across eligible agencies in step-wise allocations (water-filling algorithm).

### Complexity Analysis
- **Time Complexity:** (M \\cdot N^2)$ in the worst case for iterative water-filling step adjustments.
- **Space Complexity:** (M + N)$.

---

## 4. Fairness Metrics

### 1. Jain's Fairness Index
J(x) = \\frac{\\left( \\sum_{j=1}^n x_j \\right)^2}{n \\cdot \\sum_{j=1}^n x_j^2}
- (x) = 1.0$ indicates perfect equality across all agencies.
- (x) = 1/n$ represents maximum disparity.

### 2. Allocation Disparity
\\Delta_{\\text{alloc}} = \\max_j (x_j) - \\min_j (x_j)

---

## 5. Comparative Trade-offs Matrix

| Property | Greedy Baseline | Fairness-Aware Allocation |
| :--- | :--- | :--- |
| **Primary Objective** | Maximum throughput / priority first | Disparity reduction & equal satisfaction |
| **Algorithmic Paradigm** | Priority Sorting Greedy | Max-Min Water-Filling |
| **Time Complexity** | (M \\cdot N \\log N)$ | (M \\cdot N^2)$ |
| **Space Complexity** | (M + N)$ | (M + N)$ |
| **Fairness Consideration** | Priority score only | Explicit satisfaction ratio equalizing |
| **Main Limitation** | Low-priority agency starvation | Iterative compute overhead on large batches |
