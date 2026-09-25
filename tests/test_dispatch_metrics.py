from engine.dispatch.result import DispatchMatchDetails
from engine.metrics.dispatch import (
    compute_assignment_rate,
    compute_average_distance,
    compute_max_workload,
    compute_total_distance,
    compute_workload_distribution,
    compute_workload_variance,
)
from engine.models.location import Location
from engine.models.volunteer import Volunteer


def test_dispatch_metrics_calculations():
    m1 = DispatchMatchDetails(
        request_id='R1',
        volunteer_id='V1',
        pickup_distance_km=10.0,
        delivery_distance_km=5.0,
        total_distance_km=15.0,
    )
    m2 = DispatchMatchDetails(
        request_id='R2',
        volunteer_id='V1',
        pickup_distance_km=20.0,
        delivery_distance_km=10.0,
        total_distance_km=30.0,
    )

    matches = [m1, m2]
    assert compute_total_distance(matches) == 30.0
    assert compute_average_distance(matches) == 15.0
    assert compute_assignment_rate(2, 4) == 0.5


def test_workload_metrics():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    v1 = Volunteer(id='V1', name='Vol 1', location=loc, vehicle_capacity=100.0, current_workload=1)
    v2 = Volunteer(id='V2', name='Vol 2', location=loc, vehicle_capacity=100.0, current_workload=3)

    m1 = DispatchMatchDetails(request_id='R1', volunteer_id='V1', pickup_distance_km=5.0, total_distance_km=5.0)

    wdist = compute_workload_distribution([v1, v2], [m1])
    assert wdist['V1'] == 2
    assert wdist['V2'] == 3

    assert compute_max_workload(wdist) == 3
    assert compute_workload_variance(wdist) == 0.25
