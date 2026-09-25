import time
from datetime import datetime, timezone
from typing import List, Optional
from engine.dispatch.distance import haversine_distance
from engine.dispatch.feasibility import is_feasible
from engine.dispatch.result import DispatchBatchResult, DispatchMatchDetails
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


class ScoreBasedDispatcher:
    def __init__(
        self,
        name: str = 'Score-Based Dispatch',
        w_distance: float = 0.40,
        w_urgency: float = 0.30,
        w_workload: float = 0.20,
        w_capacity: float = 0.10,
    ):
        self.name = name
        self.w_distance = w_distance
        self.w_urgency = w_urgency
        self.w_workload = w_workload
        self.w_capacity = w_capacity

    def compute_pair_score(
        self,
        volunteer: Volunteer,
        request: RescueRequest,
        current_workload: int,
        pickup_dist: float,
        current_time: Optional[datetime] = None,
    ) -> float:
        norm_dist = min(pickup_dist / 100.0, 1.0)
        norm_workload = min(current_workload / 5.0, 1.0)

        urgency = 0.1
        if request.pickup_deadline is not None:
            now = current_time or datetime.now(timezone.utc)
            if request.pickup_deadline.tzinfo is None:
                request_dt = request.pickup_deadline.replace(tzinfo=timezone.utc)
            else:
                request_dt = request.pickup_deadline

            hours_rem = max((request_dt - now).total_seconds() / 3600.0, 0.0)
            urgency = 1.0 / (hours_rem + 1.0)

        cap_util = (
            min(request.quantity / volunteer.vehicle_capacity, 1.0)
            if volunteer.vehicle_capacity > 0
            else 0.0
        )

        score = (
            self.w_urgency * urgency
            - self.w_distance * norm_dist
            - self.w_workload * norm_workload
            + self.w_capacity * cap_util
        )
        return score

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

        unassigned_requests = {r.id: r for r in requests}
        matches: List[DispatchMatchDetails] = []

        while unassigned_requests:
            best_pair = None
            best_score = float('-inf')

            for req_id, req in list(unassigned_requests.items()):
                for v_id, state in vol_state.items():
                    if not state['is_available']:
                        continue

                    temp_vol = state['model'].model_copy(
                        update={
                            'is_available': state['is_available'],
                            'current_workload': state['current_workload'],
                        }
                    )

                    if is_feasible(temp_vol, req, current_time):
                        p_dist = haversine_distance(
                            state['location'], req.pickup_location
                        )
                        score = self.compute_pair_score(
                            temp_vol,
                            req,
                            state['current_workload'],
                            p_dist,
                            current_time,
                        )

                        if score > best_score:
                            best_score = score
                            best_pair = (req, v_id, p_dist, score)
                        elif (
                            abs(score - best_score) < 1e-9
                            and best_pair is not None
                        ):
                            if (req.id, v_id) < (best_pair[0].id, best_pair[1]):
                                best_score = score
                                best_pair = (req, v_id, p_dist, score)

            if best_pair is None:
                break

            req, best_v_id, best_p_dist, score = best_pair
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
                        'composite_score': round(score, 4),
                        'pickup_distance_km': round(best_p_dist, 3),
                        'reason': 'Max composite utility score choice',
                    },
                )
            )

            del unassigned_requests[req.id]
            vol_state[best_v_id]['current_workload'] += 1
            vol_state[best_v_id]['is_available'] = False

        unassigned_ids = list(unassigned_requests.keys())
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
