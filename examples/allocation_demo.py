import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.allocation.fair import FairnessAwareAllocator
from engine.allocation.greedy import GreedyAllocator
from engine.metrics.fairness import allocation_disparity
from engine.models.agency import Agency
from engine.models.donation import Donation
from engine.models.location import Location

def main():
    base_loc = Location(latitude=40.7128, longitude=-74.0060)
    donations = [
        Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=150.0, perishable=True, expiration_hours=24.0, requires_refrigeration=False, location=base_loc),
        Donation(id='D2', donor_id='DONOR2', food_type='dairy', quantity=100.0, perishable=True, expiration_hours=12.0, requires_refrigeration=True, location=base_loc),
        Donation(id='D3', donor_id='DONOR3', food_type='canned_goods', quantity=200.0, perishable=False, requires_refrigeration=False, location=base_loc),
    ]
    agencies = [
        Agency(id='A1', name='Community Shelter', location=base_loc, storage_capacity=200.0, current_inventory=50.0, demands=150.0, priority_score=8.0, historical_allocations=50.0, refrigeration_capable=True),
        Agency(id='A2', name='Downtown Food Bank', location=base_loc, storage_capacity=250.0, current_inventory=0.0, demands=200.0, priority_score=5.0, historical_allocations=0.0, refrigeration_capable=True),
        Agency(id='A3', name='Youth Outreach Center', location=base_loc, storage_capacity=100.0, current_inventory=20.0, demands=100.0, priority_score=3.0, historical_allocations=10.0, refrigeration_capable=False),
        Agency(id='A4', name='Senior Meal Service', location=base_loc, storage_capacity=50.0, current_inventory=0.0, demands=80.0, priority_score=9.0, historical_allocations=0.0, refrigeration_capable=False),
    ]
    greedy_res = GreedyAllocator().allocate(donations, agencies)
    fair_res = FairnessAwareAllocator().allocate(donations, agencies)
    print('======================================================================')
    print('FAIR FOOD RESOURCE ALLOCATION ENGINE -- DEMONSTRATION')
    print('======================================================================')
    def print_res(res):
        title = res.algorithm_name.upper()
        print('\n--- ' + title + ' ---')
        print('Execution Time (ms):     ' + str(round(res.execution_time_ms, 3)))
        print('Total Food Allocated:   ' + str(round(res.total_allocated, 1)) + ' kg')
        print('Unmet Demand:           ' + str(round(res.total_unmet_demand, 1)) + ' kg')
        print('Unused Supply:          ' + str(round(res.total_unused_supply, 1)) + ' kg')
        print('Jain Fairness Index:    ' + str(round(res.jain_fairness_index, 4)))
        disp = allocation_disparity(res.agency_ratios)
        print('Allocation Disparity:   ' + str(round(disp, 4)))
        print('Agency Allocations and Satisfaction Ratios:')
        for aid, r in res.agency_ratios.items():
            alloc = sum(x.allocated_quantity for x in res.allocations if x.agency_id == aid)
            aobj = next(a for a in agencies if a.id == aid)
            tot = aobj.historical_allocations + alloc
            print('  - ' + aid + ' (' + aobj.name + '): Allocated=' + str(round(alloc,1)) + ' kg, Total Recv=' + str(round(tot,1)) + ' kg, Ratio=' + str(round(r*100,2)) + '%')
    print_res(greedy_res)
    print_res(fair_res)
    print('\n======================================================================')
    print('ALGORITHM COMPARISON MATRIX')
    print('======================================================================')
    print('Total Allocated:  Greedy ' + str(round(greedy_res.total_allocated,1)) + ' kg vs Fair ' + str(round(fair_res.total_allocated,1)) + ' kg')
    print('Unmet Demand:     Greedy ' + str(round(greedy_res.total_unmet_demand,1)) + ' kg vs Fair ' + str(round(fair_res.total_unmet_demand,1)) + ' kg')
    print('Unused Supply:    Greedy ' + str(round(greedy_res.total_unused_supply,1)) + ' kg vs Fair ' + str(round(fair_res.total_unused_supply,1)) + ' kg')
    print('Jain Fairness:    Greedy ' + str(round(greedy_res.jain_fairness_index,4)) + ' vs Fair ' + str(round(fair_res.jain_fairness_index,4)))
    g_disp = allocation_disparity(greedy_res.agency_ratios)
    f_disp = allocation_disparity(fair_res.agency_ratios)
    print('Disparity:        Greedy ' + str(round(g_disp,4)) + ' vs Fair ' + str(round(f_disp,4)))
    print('Execution Time:   Greedy ' + str(round(greedy_res.execution_time_ms,3)) + ' ms vs Fair ' + str(round(fair_res.execution_time_ms,3)) + ' ms')
    print('======================================================================')

if __name__ == '__main__':
    main()
