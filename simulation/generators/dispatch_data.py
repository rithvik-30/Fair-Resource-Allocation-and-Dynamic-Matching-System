from datetime import datetime, timedelta, timezone
import random
from typing import Dict, List, Optional, Tuple

from engine.models.location import Location
from engine.models.rescue_request import RequestStatus, RescueRequest
from engine.models.volunteer import Volunteer
from simulation.generators.locations import DEFAULT_BOUNDING_BOX, generate_locations


def generate_dispatch_scenario(
    num_requests: int,
    num_volunteers: int,
    seed: Optional[int] = 42,
    bounding_box: Tuple[float, float, float, float] = DEFAULT_BOUNDING_BOX,
    base_time: Optional[datetime] = None,
) -> Tuple[List[RescueRequest], List[Volunteer]]:
    """Generates synthetic RescueRequests and Volunteers for dispatch benchmarks.

    Completely deterministic given the same seed.
    """
    rng = random.Random(seed)

    if base_time is None:
        base_time = datetime(2026, 9, 25, 10, 0, 0, tzinfo=timezone.utc)

    total_locations_needed = num_requests * 2 + num_volunteers
    locations = generate_locations(
        count=total_locations_needed,
        bounding_box=bounding_box,
        seed=rng.randint(0, 2**31 - 1),
    )

    pickup_locs = locations[:num_requests]
    dropoff_locs = locations[num_requests : num_requests * 2]
    vol_locs = locations[num_requests * 2 :]

    requests: List[RescueRequest] = []
    for i in range(num_requests):
        req_seed = rng.randint(0, 2**31 - 1)
        req_rng = random.Random(req_seed)

        qty = round(req_rng.uniform(10.0, 250.0), 1)
        req_refrig = req_rng.random() < 0.3
        p_offset = req_rng.uniform(1.0, 5.0)
        d_offset = p_offset + req_rng.uniform(1.0, 4.0)

        p_deadline = base_time + timedelta(hours=p_offset)
        d_deadline = base_time + timedelta(hours=d_offset)

        agency_idx = req_rng.randint(1, max(5, num_requests // 2))

        req = RescueRequest(
            id=f"req_{i + 1:05d}",
            donation_id=f"don_{i + 1:05d}",
            agency_id=f"agency_{agency_idx:04d}",
            pickup_location=pickup_locs[i],
            dropoff_location=dropoff_locs[i],
            quantity=qty,
            requires_refrigeration=req_refrig,
            pickup_deadline=p_deadline,
            dropoff_deadline=d_deadline,
            status=RequestStatus.PENDING,
        )
        requests.append(req)

    volunteers: List[Volunteer] = []
    capacities = [50.0, 100.0, 150.0, 250.0, 500.0]
    travel_limits = [15.0, 30.0, 50.0, 100.0, None]

    for j in range(num_volunteers):
        vol_seed = rng.randint(0, 2**31 - 1)
        vol_rng = random.Random(vol_seed)

        cap = vol_rng.choice(capacities)
        vol_refrig = vol_rng.random() < 0.35
        travel_limit = vol_rng.choice(travel_limits)

        initial_workload = vol_rng.randint(0, 3)

        vol = Volunteer(
            id=f"vol_{j + 1:05d}",
            name=f"Volunteer_{j + 1:05d}",
            location=vol_locs[j],
            vehicle_capacity=cap,
            has_refrigeration=vol_refrig,
            available_from=base_time,
            available_until=base_time + timedelta(hours=12),
            max_travel_distance=travel_limit,
            current_workload=initial_workload,
            total_distance_traveled=round(vol_rng.uniform(0.0, 40.0), 1),
            is_available=True,
        )
        volunteers.append(vol)

    return requests, volunteers
