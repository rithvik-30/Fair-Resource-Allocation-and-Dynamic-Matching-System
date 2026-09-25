from datetime import datetime
from typing import Optional, Tuple
from engine.dispatch.distance import haversine_distance
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


def check_feasibility_details(
    volunteer: Volunteer,
    request: RescueRequest,
    current_time: Optional[datetime] = None,
) -> Tuple[bool, str]:
    if not volunteer.is_available:
        return False, 'Volunteer is unavailable (is_available==False)'

    if request.quantity > volunteer.vehicle_capacity:
        return (
            False,
            f'Cargo weight ({request.quantity:.1f}kg) exceeds vehicle capacity ({volunteer.vehicle_capacity:.1f}kg)',
        )

    if request.requires_refrigeration and not volunteer.has_refrigeration:
        return (
            False,
            'Request requires cold chain refrigeration, but volunteer vehicle is not refrigeration-capable',
        )

    pickup_dist = haversine_distance(volunteer.location, request.pickup_location)

    if (
        volunteer.max_travel_distance is not None
        and volunteer.max_travel_distance > 0.0
    ):
        if pickup_dist > volunteer.max_travel_distance:
            return (
                False,
                f'Pickup distance ({pickup_dist:.2f}km) exceeds max travel distance ({volunteer.max_travel_distance:.2f}km)',
            )

    if request.pickup_deadline is not None:
        if (
            volunteer.available_until is not None
            and request.pickup_deadline > volunteer.available_until
        ):
            return (
                False,
                'Pickup deadline is after volunteer availability end',
            )
        if (
            volunteer.available_from is not None
            and request.pickup_deadline < volunteer.available_from
        ):
            return (
                False,
                'Pickup deadline is before volunteer availability start',
            )

    if current_time is not None:
        if (
            volunteer.available_until is not None
            and current_time > volunteer.available_until
        ):
            return False, 'Current time is past volunteer availability'

    return True, 'Feasible match'


def is_feasible(
    volunteer: Volunteer,
    request: RescueRequest,
    current_time: Optional[datetime] = None,
) -> bool:
    feasible, _ = check_feasibility_details(volunteer, request, current_time)
    return feasible
