import copy
import time
from typing import List, Optional
from sqlalchemy.orm import Session

from engine.allocation.fair import FairnessAwareAllocator
from engine.allocation.greedy import GreedyAllocator
from engine.metrics.fairness import allocation_disparity, jains_fairness_index
from engine.models.agency import Agency
from engine.models.donation import Donation
from backend.api.schemas.allocation import (
    AllocationComparisonResponse,
    AllocationResponse,
)
from backend.db.repositories import records


class AllocationService:
    def __init__(self):
        self.greedy_allocator = GreedyAllocator()
        self.fair_allocator = FairnessAwareAllocator()

    def _execute_allocation(
        self,
        allocator,
        donations: List[Donation],
        agencies: List[Agency],
        db: Optional[Session] = None,
    ) -> AllocationResponse:
        donations_copy = copy.deepcopy(donations)
        agencies_copy = copy.deepcopy(agencies)

        t0 = time.perf_counter()
        batch_res = allocator.allocate(donations_copy, agencies_copy)
        t1 = time.perf_counter()

        exec_time_ms = round((t1 - t0) * 1000.0, 3)

        tot_allocated = batch_res.total_allocated
        tot_unused = batch_res.total_unused_supply
        tot_unmet = batch_res.total_unmet_demand
        tot_supply = tot_allocated + tot_unused
        alloc_rate = round(tot_allocated / tot_supply, 4) if tot_supply > 0 else 0.0

        jain_idx = round(batch_res.jain_fairness_index, 4)
        disp_val = round(allocation_disparity(batch_res.agency_ratios), 4)

        if db is not None:
            for item in batch_res.allocations:
                try:
                    records.create_allocation_record(
                        db=db,
                        donation_id=item.donation_id,
                        agency_id=item.agency_id,
                        quantity_kg=item.allocated_quantity,
                        algorithm=batch_res.algorithm_name,
                    )
                except Exception:
                    pass

        return AllocationResponse(
            algorithm=batch_res.algorithm_name,
            total_supply=tot_supply,
            total_allocated=tot_allocated,
            unmet_demand=tot_unmet,
            unused_supply=tot_unused,
            allocation_rate=alloc_rate,
            jain_fairness_index=jain_idx,
            allocation_disparity=disp_val,
            execution_time_ms=batch_res.execution_time_ms if hasattr(batch_res, 'execution_time_ms') and batch_res.execution_time_ms > 0 else exec_time_ms,
            allocations=batch_res.allocations,
            agency_ratios=batch_res.agency_ratios,
        )

    def run_greedy(
        self, donations: List[Donation], agencies: List[Agency], db: Optional[Session] = None
    ) -> AllocationResponse:
        return self._execute_allocation(self.greedy_allocator, donations, agencies, db=db)

    def run_fair(
        self, donations: List[Donation], agencies: List[Agency], db: Optional[Session] = None
    ) -> AllocationResponse:
        return self._execute_allocation(self.fair_allocator, donations, agencies, db=db)

    def run_comparison(
        self, donations: List[Donation], agencies: List[Agency], db: Optional[Session] = None
    ) -> AllocationComparisonResponse:
        greedy_res = self.run_greedy(donations, agencies, db=db)
        fair_res = self.run_fair(donations, agencies, db=db)

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
