import math
import pytest
from pydantic import ValidationError

from engine.models import (
    Agency,
    AllocationResult,
    Donation,
    Donor,
    Location,
    Match,
    MatchStatus,
    RequestStatus,
    RescueRequest,
    Volunteer,
)


def test_location_valid():
    loc = Location(latitude=37.7749, longitude=-122.4194)
    assert loc.latitude == 37.7749
    assert loc.longitude == -122.4194


def test_location_invalid():
    with pytest.raises(ValidationError):
        Location(latitude=95.0, longitude=0.0)

    with pytest.raises(ValidationError):
        Location(latitude=0.0, longitude=-190.0)


def test_haversine_distance():
    nyc = Location(latitude=40.7128, longitude=-74.0060)
    la = Location(latitude=34.0522, longitude=-118.2437)

    dist = nyc.haversine_distance(la)
    assert math.isclose(dist, 3935, rel_tol=0.05)
    assert nyc.haversine_distance(nyc) == 0.0


def test_donor_creation():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    donor = Donor(id='D1', name='Fresh Market', location=loc)
    assert donor.id == 'D1'
    assert donor.operating_hours == ('08:00', '20:00')


def test_agency_capacities_and_demands():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    agency = Agency(
        id='A1',
        name='City Food Bank',
        location=loc,
        storage_capacity=500.0,
        current_inventory=100.0,
        demands=300.0,
        priority_score=8.5,
        refrigeration_capable=True,
    )
    assert agency.available_capacity == 400.0
    assert agency.unmet_demand == 300.0
    assert agency.priority_score == 8.5


def test_agency_inventory_exceeds_capacity():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    with pytest.raises(ValidationError):
        Agency(
            id='A1',
            name='City Food Bank',
            location=loc,
            storage_capacity=100.0,
            current_inventory=150.0,
            demands=50.0,
        )


def test_donation_model():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    donation = Donation(
        id='DON-1',
        donor_id='D1',
        food_type='produce',
        quantity=50.0,
        requires_refrigeration=True,
        location=loc,
    )
    assert donation.quantity == 50.0
    assert donation.requires_refrigeration is True

    with pytest.raises(ValidationError):
        Donation(
            id='DON-2',
            donor_id='D1',
            food_type='produce',
            quantity=-10.0,
        )


def test_volunteer_model():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    vol = Volunteer(
        id='V1',
        name='Alice Smith',
        location=loc,
        vehicle_capacity=200.0,
        has_refrigeration=False,
    )
    assert vol.is_available is True
    assert vol.current_workload == 0
    assert vol.vehicle_capacity == 200.0


def test_rescue_request_and_match():
    loc_donor = Location(latitude=40.7128, longitude=-74.0060)
    loc_agency = Location(latitude=40.7589, longitude=-73.9851)

    req = RescueRequest(
        id='REQ-1',
        donation_id='DON-1',
        agency_id='A1',
        pickup_location=loc_donor,
        dropoff_location=loc_agency,
        quantity=50.0,
    )
    assert req.status == RequestStatus.PENDING

    match = Match(
        id='M-1',
        request_id='REQ-1',
        volunteer_id='V1',
        estimated_distance=5.2,
    )
    assert match.status == MatchStatus.ASSIGNED
    assert match.estimated_distance == 5.2


def test_allocation_result():
    res = AllocationResult(
        donation_id='DON-1',
        agency_id='A1',
        allocated_quantity=45.5,
        explanation={'reason': 'matched priority'},
    )
    assert res.allocated_quantity == 45.5
    assert res.explanation['reason'] == 'matched priority'
