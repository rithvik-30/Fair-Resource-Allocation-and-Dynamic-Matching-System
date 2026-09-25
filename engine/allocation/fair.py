import time
from typing import Dict, List
from engine.allocation.result import AllocationBatchResult
from engine.metrics.fairness import compute_allocation_ratios, jains_fairness_index
from engine.models.agency import Agency
from engine.models.allocation_result import AllocationResult
from engine.models.donation import Donation


class FairnessAwareAllocator:
    """
    Fairness-Aware Food Resource Allocation Algorithm.

    Solves the multi-agency resource allocation problem by minimizing allocation ratio disparity.
    Uses max-min fairness (water-filling) based on the allocation ratio:
        allocation_ratio_i = (historical_allocation_i + new_allocation_i) / demand_i

    Inputs:
        donations: List[Donation]
        agencies: List[Agency]
    Outputs:
        AllocationBatchResult containing allocations, metrics, and summary execution data.

    Algorithm Steps:
        1. Sort donations by perishability and expiration time.
        2. For each donation, identify eligible recipient agencies (refrigeration, capacity, demand).
        3. Equalize satisfaction ratios across eligible agencies using max-min water-filling.
        4. Respect supply, demand, and storage capacity constraints.
        5. Compute Jain's Fairness Index and allocation ratios.

    Time Complexity: O(N_donations * N_agencies^2) worst case for water-filling iterations.
    Space Complexity: O(N_donations + N_agencies) for state tracking.
    """

    def __init__(
        self,
        name: str = "Fairness-Aware Allocation",
        use_priority_weighting: bool = True,
    ):
        self.name = name
        self.use_priority_weighting = use_priority_weighting

    def allocate(
        self, donations: List[Donation], agencies: List[Agency]
    ) -> AllocationBatchResult:
        start_time = time.perf_counter()

        rem_supply = {d.id: d.quantity for d in donations}
        rem_demand = {a.id: a.unmet_demand for a in agencies}
        rem_capacity = {a.id: a.available_capacity for a in agencies}
        total_rcvd = {a.id: a.historical_allocations for a in agencies}
        new_allocated = {a.id: 0.0 for a in agencies}

        sorted_donations = sorted(
            donations,
            key=lambda d: (
                not d.perishable,
                d.expiration_hours if d.expiration_hours is not None else float("inf"),
                d.id,
            ),
        )

        allocations_dict: Dict[str, AllocationResult] = {}

        for donation in sorted_donations:
            while rem_supply[donation.id] > 1e-6:
                eligible = [
                    a
                    for a in agencies
                    if rem_demand[a.id] > 1e-6
                    and rem_capacity[a.id] > 1e-6
                    and (
                        not donation.requires_refrigeration
                        or a.refrigeration_capable
                    )
                ]

                if not eligible:
                    break

                def get_effective_weight(a: Agency) -> float:
                    p = (
                        a.priority_score
                        if self.use_priority_weighting and a.priority_score > 0
                        else 1.0
                    )
                    return a.demands * p

                def get_adj_ratio(a: Agency) -> float:
                    r = total_rcvd[a.id] / a.demands if a.demands > 0 else 1.0
                    if self.use_priority_weighting and a.priority_score > 0:
                        return r / a.priority_score
                    return r

                min_ratio = min(get_adj_ratio(a) for a in eligible)
                min_group = [
                    a
                    for a in eligible
                    if abs(get_adj_ratio(a) - min_ratio) < 1e-9
                ]

                other_ratios = [
                    get_adj_ratio(a)
                    for a in eligible
                    if get_adj_ratio(a) > min_ratio + 1e-9
                ]
                next_ratio = min(other_ratios) if other_ratios else float("inf")

                weight_sum = sum(get_effective_weight(a) for a in min_group)
                if weight_sum <= 0:
                    break

                delta_r_supply = rem_supply[donation.id] / weight_sum
                delta_r_step = (
                    (next_ratio - min_ratio)
                    if next_ratio < float("inf")
                    else float("inf")
                )

                delta_r_caps = []
                for a in min_group:
                    max_allocatable = min(rem_demand[a.id], rem_capacity[a.id])
                    w = get_effective_weight(a)
                    if w > 0:
                        delta_r_caps.append(max_allocatable / w)

                delta_r_cap = min(delta_r_caps) if delta_r_caps else 0.0
                delta_r = min(delta_r_supply, delta_r_step, delta_r_cap)

                if delta_r <= 1e-9:
                    allocated_any = False
                    for target_agency in sorted(min_group, key=lambda a: a.id):
                        allocatable = min(
                            rem_supply[donation.id],
                            rem_demand[target_agency.id],
                            rem_capacity[target_agency.id],
                        )
                        if allocatable > 1e-6:
                            key = f"{donation.id}:{target_agency.id}"
                            if key in allocations_dict:
                                 allocations_dict[
                                     key
                                 ].allocated_quantity += allocatable
                            else:
                                 allocations_dict[key] = AllocationResult(
                                      donation_id=donation.id,
                                      agency_id=target_agency.id,
                                      allocated_quantity=allocatable,
                                      explanation={
                                          "algorithm": self.name,
                                          "priority_score": target_agency.priority_score,
                                          "reason": "fairness ratio max-min allocation",
                                     },
                                 )
                            rem_supply[donation.id] -= allocatable
                            rem_demand[target_agency.id] -= allocatable
                            rem_capacity[target_agency.id] -= allocatable
                            total_rcvd[target_agency.id] += allocatable
                            new_allocated[target_agency.id] += allocatable
                            allocated_any = True
                            break
                    if not allocated_any:
                        break
                else:
                    for a in sorted(min_group, key=lambda ag: ag.id):
                        qty = delta_r * get_effective_weight(a)
                        qty = min(
                            qty,
                            rem_supply[donation.id],
                            rem_demand[a.id],
                            rem_capacity[a.id],
                        )
                        if qty > 1e-9:
                            key = f"{donation.id}:{a.id}"
                            if key in allocations_dict:
                                 allocations_dict[key].allocated_quantity += qty
                            else:
                                 allocations_dict[key] = AllocationResult(
                                      donation_id=donation.id,
                                      agency_id=a.id,
                                      allocated_quantity=qty,
                                      explanation={
                                          "algorithm": self.name,
                                          "priority_score": a.priority_score,
                                          "reason": "fairness ratio max-min allocation",
                                     },
                                 )
                            rem_supply[donation.id] -= qty
                            rem_demand[a.id] -= qty
                            rem_capacity[a.id] -= qty
                            total_rcvd[a.id] += qty
                            new_allocated[a.id] += qty


        elapsed_ms = ((time.perf_counter() - start_time) * 1000.0)
        allocations = list(allocations_dict.values())

        total_allocated = sum(a.allocated_quantity for a in allocations)
        total_unmet_demand = sum(rem_demand.values())
        total_unused_supply = sum(rem_supply.values())

        agency_ratios = compute_allocation_ratios(agencies, allocations)
        jain_index = jains_fairness_index(agency_ratios)

        return AllocationBatchResult(
            algorithm_name=self.name,
            allocations=allocations,
            total_allocated=total_allocated,
            total_unmet_demand=total_unmet_demand,
            total_unused_supply=total_unused_supply,
            execution_time_ms=elapsed_ms,
            agency_ratios=agency_ratios,
            jain_fairness_index=jain_index,
        )
