from datetime import datetime, timezone, timedelta
from engine.dispatch.feasibility import check_feasibility_details, is_feasible
from engine.models.location import Location
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


def test_feasible_pair():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    v = Volunteer(id='V1', name='Vol 1', location=loc, vehicle_capacity=100.0, has_refrigeration=True)
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=loc,
        dropoff_location=loc,
        quantity=50.0,
        requires_refrigeration=True,
    )
    assert is_feasible(v, r) is True


def test_capacity_violation():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    v = Volunteer(id='V1', name='Vol 1', location=loc, vehicle_capacity=50.0)
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=loc,
        dropoff_location=loc,
        quantity=100.0,
    )
    feasible, reason = check_feasibility_details(v, r)
    assert feasible is False
    assert 'capacity' in reason.lower()


def test_refrigeration_violation():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    v = Volunteer(id='V1', name='Vol 1', location=loc, vehicle_capacity=100.0, has_refrigeration=False)
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=loc,
        dropoff_location=loc,
        quantity=50.0,
        requires_refrigeration=True,
    )
    feasible, reason = check_feasibility_details(v, r)
    assert feasible is False
    assert 'refrigeration' in reason.lower()


def test_unavailable_volunteer():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    v = Volunteer(id='V1', name='Vol 1', location=loc, vehicle_capacity=100.0, is_available=False)
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=loc,
        dropoff_location=loc,
        quantity=50.0,
    )
    feasible, reason = check_feasibility_details(v, r)
    assert feasible is False
    assert 'unavailable' in reason.lower()


def test_max_distance_violation():
    loc_a = Location(latitude=40.7128, longitude=-74.0060)
    loc_b = Location(latitude=42.3601, longitude=-71.0589)
    v = Volunteer(id='V1', name='Vol 1', location=loc_a, vehicle_capacity=100.0, max_travel_distance=50.0)
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=loc_b,
        dropoff_location=loc_b,
        quantity=50.0,
    )
    feasible, reason = check_feasibility_details(v, r)
    assert feasible is False
    assert 'distance' in reason.lower()
