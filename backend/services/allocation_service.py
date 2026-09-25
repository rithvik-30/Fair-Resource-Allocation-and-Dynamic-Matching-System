import copy
import time
from typing import List

from engine.allocation.fair import FairnessAwareAllocator
from engine.allocation.greedy import GreedyAllocator
from engine.metrics.fairness import allocation_disparity
from engine.models.agency import Agency
from engine.models.donation import Donation
from backend.api.schemas.allocation import (
    AllocationComparisonResponse,
    AllocationResponse,
)


class AllocationService:
    def __init__(self):
        self.greedy_allocator = GreedyAllocator()
        self.fair_allocator = FairnessAwareAllocator()

    def _execute_allocation(
        self,
        allocator,
        donations: List[Donation],
        agencies: List[Agency],
    ) -> AllocationResponse:
        donations_copy = copy.deepcopy(donations)
        agencies_copy = copy.deepcopy(agencies)

        total_supply = sum(d.quantity for d in donations_copy)

        t0 = time.perf_counter()
        batch_res = allocator.allocate(donations_copy, agencies_copy)
        t1 = time.perf_counter()

        exec_time_ms = round((t1 - t0) * 1000.0, 3)

        total_allocated = batch_res.total_allocated
        alloc_rate = (
            round(total_allocated / total_supply, 4) if total_supply > 0 else 0.0
        )
        disp_val = round(allocation_disparity(batch_res.agency_ratios), 4)

        return AllocationResponse(
            algorithm=batch_res.algorithm_name,
            total_supply=total_supply,
            total_allocated=total_allocated,
            unmet_demand=batch_res.total_unmet_demand,
            unused_supply=batch_res.total_unused_supply,
            allocation_rate=alloc_rate,
            jain_fairness_index=round(batch_res.jain_fairness_index, 4),
            allocation_disparity=disp_val,
            execution_time_ms=exec_time_ms,
            allocations=batch_res.allocations,
            agency_ratios=batch_res.agency_ratios,
        )

    def run_greedy(
        self, donations: List[Donation], agencies: List[Agency]
    ) -> AllocationResponse:
        return self._execute_allocation(self.greedy_allocator, donations, agencies)

    def run_fair(
        self, donations: List[Donation], agencies: List[Agency]
    ) -> AllocationResponse:
        return self._execute_allocation(self.fair_allocator, donations, agencies)

    def run_comparison(
        self, donations: List[Donation], agencies: List[Agency]
    ) -> AllocationComparisonResponse:
        greedy_res = self.run_greedy(donations, agencies)
        fair_res = self.run_fair(donations, agencies)

        summary = {
            "total_supply": greedy_res.total_supply,
            "greedy_allocated": greedy_res.total_allocated,
            "fairness_aware_allocated": fair_res.total_allocated,
            "greedy_jain_index": greedy_res.jain_fairness_index,
            "fairness_aware_jain_index": fair_res.jain_fairness_index,
            "fairness_gain": round(
                fair_res.jain_fairness_index - greedy_res.jain_fairness_index, 4
            ),
        }

        return AllocationComparisonResponse(
            greedy=greedy_res,
            fairness_aware=fair_res,
            comparison_summary=summary,
        )
