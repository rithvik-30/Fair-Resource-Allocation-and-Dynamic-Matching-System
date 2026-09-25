from datetime import datetime, timezone, timedelta
import pytest
from engine.dispatch import (
    BatchBipartiteDispatcher,
    NearestVolunteerDispatcher,
    ScoreBasedDispatcher,
)
from engine.models.location import Location
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


@pytest.fixture
def base_loc():
    return Location(latitude=40.7128, longitude=-74.0060)


@pytest.fixture
def far_loc():
    return Location(latitude=41.1500, longitude=-74.0060)


# --- NEAREST VOLUNTEER DISPATCHER TESTS ---


def test_nearest_chooses_closest_feasible(base_loc, far_loc):
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=50.0,
    )
    v_near = Volunteer(id='V_NEAR', name='Near', location=base_loc, vehicle_capacity=100.0)
    v_far = Volunteer(id='V_FAR', name='Far', location=far_loc, vehicle_capacity=100.0)

    dispatcher = NearestVolunteerDispatcher()
    res = dispatcher.dispatch([r], [v_far, v_near])

    assert res.total_assigned == 1
    assert res.matches[0].volunteer_id == 'V_NEAR'


def test_nearest_ignores_infeasible_closer_volunteer(base_loc, far_loc):
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=150.0,
    )
    v_near = Volunteer(id='V_NEAR', name='Near Small', location=base_loc, vehicle_capacity=100.0)
    v_far = Volunteer(id='V_FAR', name='Far Large', location=far_loc, vehicle_capacity=200.0)

    dispatcher = NearestVolunteerDispatcher()
    res = dispatcher.dispatch([r], [v_near, v_far])

    assert res.total_assigned == 1
    assert res.matches[0].volunteer_id == 'V_FAR'


def test_nearest_deterministic_tie_breaking(base_loc):
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=50.0,
    )
    v_b = Volunteer(id='V_B', name='Vol B', location=base_loc, vehicle_capacity=100.0)
    v_a = Volunteer(id='V_A', name='Vol A', location=base_loc, vehicle_capacity=100.0)

    dispatcher = NearestVolunteerDispatcher()
    res = dispatcher.dispatch([r], [v_b, v_a])

    assert res.total_assigned == 1
    assert res.matches[0].volunteer_id == 'V_A'


# --- SCORE-BASED DISPATCHER TESTS ---


def test_score_based_determinism(base_loc, far_loc):
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=50.0,
    )
    v1 = Volunteer(id='V1', name='Vol 1', location=base_loc, vehicle_capacity=100.0)
    v2 = Volunteer(id='V2', name='Vol 2', location=far_loc, vehicle_capacity=100.0)

    dispatcher = ScoreBasedDispatcher()
    res1 = dispatcher.dispatch([r], [v1, v2])
    res2 = dispatcher.dispatch([r], [v1, v2])

    assert res1.matches[0].volunteer_id == res2.matches[0].volunteer_id


def test_score_based_workload_impact(base_loc):
    r = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=50.0,
    )
    v1 = Volunteer(id='V1', name='Busy', location=base_loc, vehicle_capacity=100.0, current_workload=5)
    v2 = Volunteer(id='V2', name='Free', location=base_loc, vehicle_capacity=100.0, current_workload=0)

    dispatcher = ScoreBasedDispatcher()
    res = dispatcher.dispatch([r], [v1, v2])

    assert res.total_assigned == 1
    assert res.matches[0].volunteer_id == 'V2'


def test_score_based_urgency_impact(base_loc, far_loc):
    now = datetime.now(timezone.utc)
    r_urgent = RescueRequest(
        id='R_URGENT',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=50.0,
        pickup_deadline=now + timedelta(minutes=5),
    )
    r_normal = RescueRequest(
        id='R_NORMAL',
        donation_id='D2',
        agency_id='A2',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=50.0,
        pickup_deadline=now + timedelta(hours=24),
    )
    v = Volunteer(id='V1', name='Vol', location=base_loc, vehicle_capacity=100.0)

    dispatcher = ScoreBasedDispatcher(w_urgency=0.8, w_distance=0.1)
    res = dispatcher.dispatch([r_urgent, r_normal], [v], current_time=now)

    assert res.total_assigned == 1
    assert res.matches[0].request_id == 'R_URGENT'


# --- BATCH BIPARTITE MATCHING TESTS ---


def test_batch_matching_feasible_only(base_loc):
    r1 = RescueRequest(
        id='R1',
        donation_id='D1',
        agency_id='A1',
        pickup_location=base_loc,
        dropoff_location=base_loc,
        quantity=150.0,
        requires_refrigeration=True,
    )
    v_infeasible = Volunteer(
        id='V1', name='No Refrig', location=base_loc, vehicle_capacity=200.0, has_refrigeration=False
    )

    dispatcher = BatchBipartiteDispatcher()
    res = dispatcher.dispatch([r1], [v_infeasible])

    assert res.total_assigned == 0
    assert len(res.unassigned_request_ids) == 1


def test_batch_matching_no_double_assignment(base_loc):
    r1 = RescueRequest(id='R1', donation_id='D1', agency_id='A1', pickup_location=base_loc, dropoff_location=base_loc, quantity=50.0)
    r2 = RescueRequest(id='R2', donation_id='D2', agency_id='A2', pickup_location=base_loc, dropoff_location=base_loc, quantity=50.0)
    v1 = Volunteer(id='V1', name='Single Vol', location=base_loc, vehicle_capacity=100.0)

    dispatcher = BatchBipartiteDispatcher()
    res = dispatcher.dispatch([r1, r2], [v1])

    assert res.total_assigned == 1
    assert res.total_unassigned == 1


# --- GENERAL & EDGE CASES ---


def test_empty_requests(base_loc):
    v1 = Volunteer(id='V1', name='Vol', location=base_loc, vehicle_capacity=100.0)
    for dispatcher in [NearestVolunteerDispatcher(), ScoreBasedDispatcher(), BatchBipartiteDispatcher()]:
        res = dispatcher.dispatch([], [v1])
        assert res.total_assigned == 0
        assert res.total_unassigned == 0


def test_empty_volunteers(base_loc):
    r1 = RescueRequest(id='R1', donation_id='D1', agency_id='A1', pickup_location=base_loc, dropoff_location=base_loc, quantity=50.0)
    for dispatcher in [NearestVolunteerDispatcher(), ScoreBasedDispatcher(), BatchBipartiteDispatcher()]:
        res = dispatcher.dispatch([r1], [])
        assert res.total_assigned == 0
        assert res.total_unassigned == 1


def test_multiple_requests_and_volunteers(base_loc, far_loc):
    r1 = RescueRequest(id='R1', donation_id='D1', agency_id='A1', pickup_location=base_loc, dropoff_location=base_loc, quantity=50.0)
    r2 = RescueRequest(id='R2', donation_id='D2', agency_id='A2', pickup_location=far_loc, dropoff_location=far_loc, quantity=60.0)

    v1 = Volunteer(id='V1', name='Vol 1', location=base_loc, vehicle_capacity=100.0)
    v2 = Volunteer(id='V2', name='Vol 2', location=far_loc, vehicle_capacity=100.0)

    for dispatcher in [NearestVolunteerDispatcher(), ScoreBasedDispatcher(), BatchBipartiteDispatcher()]:
        res = dispatcher.dispatch([r1, r2], [v1, v2])
        assert res.total_assigned == 2
        assert res.total_unassigned == 0
