import time
from typing import List
from engine.allocation.result import AllocationBatchResult
from engine.metrics.fairness import compute_allocation_ratios, jains_fairness_index
from engine.models.agency import Agency
from engine.models.allocation_result import AllocationResult
from engine.models.donation import Donation


class GreedyAllocator:
    """Greedy Baseline Food Allocation Algorithm."""

    def __init__(self, name: str = "Greedy Allocation Baseline"):
        self.name = name

    def allocate(
        self, donations: List[Donation], agencies: List[Agency]
    ) -> AllocationBatchResult:
        start_time = time.perf_counter()

        rem_supply = {d.id: d.quantity for d in donations}
        rem_demand = {a.id: a.unmet_demand for a in agencies}
        rem_capacity = {a.id: a.available_capacity for a in agencies}

        sorted_donations = sorted(
            donations,
            key=lambda d: (
                not d.perishable,
                d.expiration_hours if d.expiration_hours is not None else float("inf"),
                d.id,
            ),
        )

        allocations: List[AllocationResult] = []

        for donation in sorted_donations:
            if rem_supply[donation.id] <= 0:
                continue

            sorted_agencies = sorted(
                agencies,
                key=lambda a: (-a.priority_score, a.id),
            )

            for agency in sorted_agencies:
                if rem_supply[donation.id] <= 0:
                    break

                if donation.requires_refrigeration and not agency.refrigeration_capable:
                    continue

                allocatable = min(
                    rem_supply[donation.id],
                    rem_demand[agency.id],
                    rem_capacity[agency.id],
                )

                if allocatable > 0:
                    allocations.append(
                        AllocationResult(
                            donation_id=donation.id,
                            agency_id=agency.id,
                            allocated_quantity=allocatable,
                            explanation={
                                "algorithm": self.name,
                                "priority_score": agency.priority_score,
                                "reason": "greedy priority match",
                            },
                        )
                    )
                    rem_supply[donation.id] -= allocatable
                    rem_demand[agency.id] -= allocatable
                    rem_capacity[agency.id] -= allocatable

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

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
