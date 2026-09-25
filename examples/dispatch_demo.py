import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime, timezone, timedelta
from engine.dispatch import (
    BatchBipartiteDispatcher,
    NearestVolunteerDispatcher,
    ScoreBasedDispatcher,
)
from engine.models.location import Location
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer


def run_dispatch_demo():
    print('========================================================================')
    print('       DYNAMIC VOLUNTEER DISPATCH ENGINE - DEMONSTRATION')
    print('========================================================================\n')

    now = datetime.now(timezone.utc)

    loc_hub = Location(latitude=40.7128, longitude=-74.0060)
    loc_downtown = Location(latitude=40.7050, longitude=-74.0090)
    loc_uptown = Location(latitude=40.7831, longitude=-73.9712)
    loc_queens = Location(latitude=40.7282, longitude=-73.7949)
    loc_brooklyn = Location(latitude=40.6782, longitude=-73.9442)

    requests = [
        RescueRequest(
            id='REQ_01',
            donation_id='DON_01',
            agency_id='AG_01',
            pickup_location=loc_downtown,
            dropoff_location=loc_uptown,
            quantity=80.0,
            requires_refrigeration=True,
            pickup_deadline=now + timedelta(minutes=45),
        ),
        RescueRequest(
            id='REQ_02',
            donation_id='DON_02',
            agency_id='AG_02',
            pickup_location=loc_uptown,
            dropoff_location=loc_queens,
            quantity=150.0,
            requires_refrigeration=False,
            pickup_deadline=now + timedelta(hours=4),
        ),
        RescueRequest(
            id='REQ_03',
            donation_id='DON_03',
            agency_id='AG_03',
            pickup_location=loc_brooklyn,
            dropoff_location=loc_hub,
            quantity=40.0,
            requires_refrigeration=False,
            pickup_deadline=now + timedelta(hours=2),
        ),
        RescueRequest(
            id='REQ_04',
            donation_id='DON_04',
            agency_id='AG_04',
            pickup_location=loc_queens,
            dropoff_location=loc_downtown,
            quantity=200.0,
            requires_refrigeration=True,
            pickup_deadline=now + timedelta(hours=1),
        ),
        RescueRequest(
            id='REQ_05',
            donation_id='DON_05',
            agency_id='AG_05',
            pickup_location=loc_hub,
            dropoff_location=loc_brooklyn,
            quantity=60.0,
            requires_refrigeration=False,
            pickup_deadline=now + timedelta(hours=6),
        ),
    ]

    volunteers = [
        Volunteer(
            id='VOL_01',
            name='Alice (Van, Cold Chain)',
            location=loc_hub,
            vehicle_capacity=250.0,
            has_refrigeration=True,
            is_available=True,
            current_workload=2,
            max_travel_distance=50.0,
        ),
        Volunteer(
            id='VOL_02',
            name='Bob (Sedan, Standard)',
            location=loc_downtown,
            vehicle_capacity=100.0,
            has_refrigeration=False,
            is_available=True,
            current_workload=0,
            max_travel_distance=30.0,
        ),
        Volunteer(
            id='VOL_03',
            name='Charlie (Refrigerated Truck)',
            location=loc_queens,
            vehicle_capacity=300.0,
            has_refrigeration=True,
            is_available=True,
            current_workload=1,
            max_travel_distance=40.0,
        ),
        Volunteer(
            id='VOL_04',
            name='Diana (Compact Car)',
            location=loc_uptown,
            vehicle_capacity=50.0,
            has_refrigeration=False,
            is_available=True,
            current_workload=0,
            max_travel_distance=25.0,
        ),
        Volunteer(
            id='VOL_05',
            name='Evan (SUV, Standard)',
            location=loc_brooklyn,
            vehicle_capacity=120.0,
            has_refrigeration=False,
            is_available=True,
            current_workload=3,
            max_travel_distance=35.0,
        ),
    ]

    print(f'Total Rescue Requests: {len(requests)}')
    print(f'Total Available Volunteers: {len(volunteers)}\n')

    dispatchers = [
        NearestVolunteerDispatcher(),
        ScoreBasedDispatcher(w_distance=0.4, w_urgency=0.3, w_workload=0.2, w_capacity=0.1),
        BatchBipartiteDispatcher(workload_penalty_weight=2.0),
    ]

    results = []
    for dispatcher in dispatchers:
        res = dispatcher.dispatch(requests, volunteers, current_time=now)
        results.append(res)

    print('=' * 95)
    print('| Algorithm                  | Assigned | Unassigned | Total Dist (km) | Avg Dist (km) | Workload Var |')
    print('=' * 95)

    for r in results:
        print(f'| {r.algorithm_name:<26} | {r.total_assigned:<8} | {r.total_unassigned:<10} | {r.total_distance_km:<15.2f} | {r.average_distance_km:<13.2f} | {r.workload_variance:<12.4f} |')

    print('=' * 95)
    print('\nAlgorithmic Trade-Off Summary:')
    print('- Nearest Volunteer Greedy: Fast local pickup distance minimization; ignores global workload/urgency balance.')
    print('- Score-Based Dispatch: Multi-criteria optimization balancing distance, deadline urgency, workload, and capacity.')
    print('- Batch Bipartite Matching: Formulates global assignment as min-weight matching via Hungarian Algorithm.\n')


if __name__ == '__main__':
    run_dispatch_demo()
