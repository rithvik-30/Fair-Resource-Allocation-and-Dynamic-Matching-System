import copy
from datetime import datetime, timezone
import time
from typing import List, Optional
from sqlalchemy.orm import Session

from engine.dispatch.batch_matching import BatchBipartiteDispatcher
from engine.dispatch.nearest import NearestVolunteerDispatcher
from engine.dispatch.scored import ScoreBasedDispatcher
from engine.metrics.dispatch import (
    compute_assignment_rate,
    compute_max_workload,
    compute_workload_distribution,
    compute_workload_variance,
)
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer
from backend.api.schemas.dispatch import (
    DispatchComparisonResponse,
    DispatchMatchResponse,
    DispatchResponse,
)
from backend.db.repositories import records


class DispatchService:
    def __init__(self):
        self.nearest_dispatcher = NearestVolunteerDispatcher()
        self.scored_dispatcher = ScoreBasedDispatcher()
        self.batch_dispatcher = BatchBipartiteDispatcher()

    def _execute_dispatch(
        self,
        dispatcher,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
        db: Optional[Session] = None,
    ) -> DispatchResponse:
        reqs_copy = copy.deepcopy(requests)
        vols_copy = copy.deepcopy(volunteers)

        if current_time is None:
            current_time = datetime(2026, 9, 25, 10, 0, 0, tzinfo=timezone.utc)

        t0 = time.perf_counter()
        batch_res = dispatcher.dispatch(
            requests=reqs_copy,
            volunteers=vols_copy,
            current_time=current_time,
        )
        t1 = time.perf_counter()

        exec_time_ms = round((t1 - t0) * 1000.0, 3)

        total_reqs = len(requests)
        assigned_cnt = batch_res.total_assigned
        unassigned_cnt = batch_res.total_unassigned
        assign_rate = round(compute_assignment_rate(assigned_cnt, total_reqs), 4)

        workload_dist = compute_workload_distribution(vols_copy, batch_res.matches)
        wl_var = round(compute_workload_variance(workload_dist), 4)
        max_wl = compute_max_workload(workload_dist)

        matches_schema = [
            DispatchMatchResponse(
                request_id=m.request_id,
                volunteer_id=m.volunteer_id,
                pickup_distance_km=round(m.pickup_distance_km, 2),
                dropoff_distance_km=round(m.delivery_distance_km, 2),
                total_distance_km=round(m.total_distance_km, 2),
                is_feasible=True,
                feasibility_reasons=[f"{k}: {v}" for k, v in m.explanation.items()],
            )
            for m in batch_res.matches
        ]

        if db is not None:
            for m in batch_res.matches:
                try:
                    records.create_dispatch_record(
                        db=db,
                        rescue_request_id=m.request_id,
                        volunteer_id=m.volunteer_id,
                        algorithm=batch_res.algorithm_name,
                        distance_km=round(m.total_distance_km, 2),
                    )
                except Exception:
                    pass

        return DispatchResponse(
            algorithm=batch_res.algorithm_name,
            assigned_requests_count=assigned_cnt,
            unassigned_requests_count=unassigned_cnt,
            assignment_rate=assign_rate,
            total_distance_km=round(batch_res.total_distance_km, 2),
            average_distance_km=round(batch_res.average_distance_km, 2),
            workload_variance=wl_var,
            max_workload=max_wl,
            execution_time_ms=exec_time_ms,
            matches=matches_schema,
            unassigned_request_ids=batch_res.unassigned_request_ids,
        )

    def run_nearest(
        self,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
        db: Optional[Session] = None,
    ) -> DispatchResponse:
        return self._execute_dispatch(
            self.nearest_dispatcher, requests, volunteers, current_time, db=db
        )

    def run_scored(
        self,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
        db: Optional[Session] = None,
    ) -> DispatchResponse:
        return self._execute_dispatch(
            self.scored_dispatcher, requests, volunteers, current_time, db=db
        )

    def run_batch(
        self,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
        db: Optional[Session] = None,
    ) -> DispatchResponse:
        return self._execute_dispatch(
            self.batch_dispatcher, requests, volunteers, current_time, db=db
        )

    def run_comparison(
        self,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
        db: Optional[Session] = None,
    ) -> DispatchComparisonResponse:
        nearest_res = self.run_nearest(requests, volunteers, current_time, db=db)
        scored_res = self.run_scored(requests, volunteers, current_time, db=db)
        batch_res = self.run_batch(requests, volunteers, current_time, db=db)

        summary = {
            "total_requests": len(requests),
            "total_volunteers": len(volunteers),
            "assignment_rates": {
                "nearest": nearest_res.assignment_rate,
                "scored": scored_res.assignment_rate,
                "batch_bipartite": batch_res.assignment_rate,
            },
            "total_distances_km": {
                "nearest": nearest_res.total_distance_km,
                "scored": scored_res.total_distance_km,
                "batch_bipartite": batch_res.total_distance_km,
            },
            "workload_variances": {
                "nearest": nearest_res.workload_variance,
                "scored": scored_res.workload_variance,
                "batch_bipartite": batch_res.workload_variance,
            },
        }

        return DispatchComparisonResponse(
            nearest=nearest_res,
            scored=scored_res,
            batch_bipartite=batch_res,
            comparison_summary=summary,
        )
