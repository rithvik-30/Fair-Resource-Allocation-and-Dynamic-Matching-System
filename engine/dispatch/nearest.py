import time
from datetime import datetime, timezone
from typing import List, Optional
from engine.dispatch.distance import haversine_distance
from engine.dispatch.feasibility import is_feasible
from engine.dispatch.result import DispatchBatchResult, DispatchMatchDetails
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


class NearestVolunteerDispatcher:
    def __init__(self, name: str = 'Nearest Volunteer Greedy'):
        self.name = name

    def dispatch(
        self,
        requests: List[RescueRequest],
        volunteers: List[Volunteer],
        current_time: Optional[datetime] = None,
    ) -> DispatchBatchResult:
        start_time = time.perf_counter()

        vol_state = {
            v.id: {
                'model': v,
                'is_available': v.is_available,
                'current_workload': v.current_workload,
                'location': v.location,
            }
            for v in volunteers
        }

        sorted_requests = sorted(
            requests,
            key=lambda r: (
                r.pickup_deadline if r.pickup_deadline is not None else datetime.max.replace(tzinfo=timezone.utc),
                r.id,
            ),
        )

        matches: List[DispatchMatchDetails] = []
        unassigned_ids: List[str] = []

        for req in sorted_requests:
            feasible_candidates = []
            for v_id, state in vol_state.items():
                if not state['is_available']:
                    continue

                temp_vol = state['model'].model_copy(
                    update={
                        'is_available': state['is_available'],
                        'current_workload': state['current_workload'],
                    }
                )

                if is_feasible(temp_vol, req):
                    p_dist = haversine_distance(state['location'], req.pickup_location)
                    feasible_candidates.append((p_dist, v_id, temp_vol))

            if not feasible_candidates:
                unassigned_ids.append(req.id)
                continue

            feasible_candidates.sort(key=lambda item: (item[0], item[1]))
            best_p_dist, best_v_id, best_vol = feasible_candidates[0]

            d_dist = haversine_distance(req.pickup_location, req.dropoff_location)
            tot_dist = best_p_dist + d_dist

            matches.append(
                DispatchMatchDetails(
                    request_id=req.id,
                    volunteer_id=best_v_id,
                    pickup_distance_km=best_p_dist,
                    delivery_distance_km=d_dist,
                    total_distance_km=tot_dist,
                    explanation={
                        'algorithm': self.name,
                        'pickup_distance_km': round(best_p_dist, 3),
                        'reason': 'Minimum pickup distance greedy choice',
                    },
                )
            )

            vol_state[best_v_id]['current_workload'] += 1
            vol_state[best_v_id]['is_available'] = False

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        tot_pickup_dist = sum(m.pickup_distance_km for m in matches)
        avg_dist = tot_pickup_dist / len(matches) if matches else 0.0

        final_workloads = [s['current_workload'] for s in vol_state.values()]
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
