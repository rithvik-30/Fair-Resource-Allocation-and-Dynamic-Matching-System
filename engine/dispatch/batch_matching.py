from datetime import datetime
import time
from typing import List, Optional
import numpy as np
from scipy.optimize import linear_sum_assignment
from engine.dispatch.distance import haversine_distance
from engine.dispatch.feasibility import is_feasible
from engine.dispatch.result import DispatchBatchResult, DispatchMatchDetails
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


class BatchBipartiteDispatcher:
    def __init__(
        self,
        name: str = 'Batch Bipartite Matching',
        workload_penalty_weight: float = 2.0,
    ):
        self.name = name
        self.workload_penalty_weight = workload_penalty_weight

    def dispatch(
        self,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
    ) -> DispatchBatchResult:
        start_time = time.perf_counter()

        if not requests or not volunteers:
            return DispatchBatchResult(
                algorithm_name=self.name,
                matches=[],
                unassigned_request_ids=[r.id for r in requests],
                total_distance_km=0.0,
                average_distance_km=0.0,
                total_assigned=0,
                total_unassigned=len(requests),
                workload_variance=0.0,
                execution_time_ms=(time.perf_counter() - start_time) * 1000.0,
            )

        sorted_requests = sorted(requests, key=lambda r: r.id)
        available_volunteers = [v for v in volunteers if v.is_available]
        sorted_volunteers = sorted(available_volunteers, key=lambda v: v.id)

        m = len(sorted_requests)
        n = len(sorted_volunteers)

        if n == 0:
            return DispatchBatchResult(
                algorithm_name=self.name,
                matches=[],
                unassigned_request_ids=[r.id for r in sorted_requests],
                total_distance_km=0.0,
                average_distance_km=0.0,
                total_assigned=0,
                total_unassigned=m,
                workload_variance=0.0,
                execution_time_ms=(time.perf_counter() - start_time) * 1000.0,
            )

        INF_COST = 1e9
        cost_matrix = np.full((m, n), INF_COST, dtype=np.float64)

        for i, req in enumerate(sorted_requests):
            for j, vol in enumerate(sorted_volunteers):
                if is_feasible(vol, req):
                    p_dist = haversine_distance(vol.location, req.pickup_location)
                    cost = p_dist + self.workload_penalty_weight * vol.current_workload
                    cost_matrix[i, j] = cost

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        matches: List[DispatchMatchDetails] = []
        assigned_req_indices = set()
        vol_workload_updates = {v.id: v.current_workload for v in volunteers}

        for r_idx, c_idx in zip(row_ind, col_ind):
            cost = cost_matrix[r_idx, c_idx]
            if cost >= INF_COST / 2.0:
                continue

            req = sorted_requests[r_idx]
            vol = sorted_volunteers[c_idx]

            p_dist = haversine_distance(vol.location, req.pickup_location)
            d_dist = haversine_distance(req.pickup_location, req.dropoff_location)
            tot_dist = p_dist + d_dist

            matches.append(
                DispatchMatchDetails(
                    request_id=req.id,
                    volunteer_id=vol.id,
                    pickup_distance_km=p_dist,
                    delivery_distance_km=d_dist,
                    total_distance_km=tot_dist,
                    explanation={
                        'algorithm': self.name,
                        'bipartite_edge_cost': round(cost, 3),
                        'pickup_distance_km': round(p_dist, 3),
                        'reason': 'Global minimum weight bipartite matching',
                    },
                )
            )

            assigned_req_indices.add(r_idx)
            vol_workload_updates[vol.id] += 1

        unassigned_ids = [
            sorted_requests[i].id
            for i in range(m)
            if i not in assigned_req_indices
        ]

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        tot_pickup_dist = sum(m.pickup_distance_km for m in matches)
        avg_dist = tot_pickup_dist / len(matches) if matches else 0.0

        final_workloads = list(vol_workload_updates.values())
        mean_w = sum(final_workloads) / len(final_workloads) if final_workloads else 0.0
        w_var = (
            sum((w - mean_w) ** 2 for w in final_workloads) / len(final_workloads)
            if final_workloads
            else 0.0
        )

        return DispatchBatchResult(
            algorithm_name=self.name,
            matches=matches,
            unassigned_request_ids=unassigned_ids,
            total_distance_km=tot_pickup_dist,
            average_distance_km=avg_dist,
            total_assigned=len(matches),
            total_unassigned=len(unassigned_ids),
            workload_variance=w_var,
            execution_time_ms=elapsed_ms,
        )
