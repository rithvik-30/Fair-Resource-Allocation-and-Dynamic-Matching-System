import pytest
from engine.allocation import FairnessAwareAllocator, GreedyAllocator
from engine.models import Agency, Donation, Location


@pytest.fixture
def base_location():
    return Location(latitude=40.7128, longitude=-74.0060)


def test_supply_constraint(base_location):
    d = Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=50.0, location=base_location)
    a1 = Agency(id='A1', name='Agency 1', location=base_location, storage_capacity=100.0, demands=100.0)

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res = allocator.allocate([d], [a1])
        assert res.total_allocated <= 50.0
        assert res.total_unused_supply >= 0.0


def test_demand_constraint(base_location):
    d = Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=200.0, location=base_location)
    a1 = Agency(id='A1', name='Agency 1', location=base_location, storage_capacity=200.0, demands=50.0)

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res = allocator.allocate([d], [a1])
        alloc_a1 = sum(item.allocated_quantity for item in res.allocations if item.agency_id == 'A1')
        assert alloc_a1 <= 50.0


def test_storage_constraint(base_location):
    d = Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=200.0, location=base_location)
    a1 = Agency(id='A1', name='Agency 1', location=base_location, storage_capacity=30.0, current_inventory=10.0, demands=100.0)

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res = allocator.allocate([d], [a1])
        alloc_a1 = sum(item.allocated_quantity for item in res.allocations if item.agency_id == 'A1')
        assert alloc_a1 <= 20.0  # available capacity = 30 - 10 = 20


def test_refrigeration_constraint(base_location):
    d_chilled = Donation(id='D1', donor_id='DONOR1', food_type='dairy', quantity=50.0, requires_refrigeration=True, location=base_location)
    a_dry = Agency(id='A1', name='Dry Only Agency', location=base_location, storage_capacity=100.0, demands=100.0, refrigeration_capable=False)
    a_cold = Agency(id='A2', name='Cold Capable Agency', location=base_location, storage_capacity=100.0, demands=100.0, refrigeration_capable=True)

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res = allocator.allocate([d_chilled], [a_dry, a_cold])
        alloc_dry = sum(item.allocated_quantity for item in res.allocations if item.agency_id == 'A1')
        alloc_cold = sum(item.allocated_quantity for item in res.allocations if item.agency_id == 'A2')
        assert alloc_dry == 0.0
        assert alloc_cold == 50.0


def test_zero_supply(base_location):
    a1 = Agency(id='A1', name='Agency 1', location=base_location, storage_capacity=100.0, demands=100.0)

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res = allocator.allocate([], [a1])
        assert res.total_allocated == 0.0
        assert len(res.allocations) == 0


def test_zero_demand(base_location):
    d = Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=50.0, location=base_location)
    a_zero = Agency(id='A1', name='Zero Demand Agency', location=base_location, storage_capacity=100.0, demands=0.0)

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res = allocator.allocate([d], [a_zero])
        assert res.total_allocated == 0.0


def test_competing_agencies_limited_supply(base_location):
    d = Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=60.0, location=base_location)
    a1 = Agency(id='A1', name='Agency 1', location=base_location, storage_capacity=100.0, demands=50.0, priority_score=9.0)
    a2 = Agency(id='A2', name='Agency 2', location=base_location, storage_capacity=100.0, demands=50.0, priority_score=5.0)

    greedy = GreedyAllocator()
    res_greedy = greedy.allocate([d], [a1, a2])
    assert res_greedy.total_allocated == 60.0

    fair = FairnessAwareAllocator()
    res_fair = fair.allocate([d], [a1, a2])
    assert res_fair.total_allocated == 60.0


def test_fairness_behavior_contrast(base_location):
    d = Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=100.0, location=base_location)
    # Both have demand 100. A1 has priority 10.0, A2 has priority 1.0. Both historical allocations 0.
    a1 = Agency(id='A1', name='High Priority', location=base_location, storage_capacity=200.0, demands=100.0, priority_score=10.0)
    a2 = Agency(id='A2', name='Low Priority', location=base_location, storage_capacity=200.0, demands=100.0, priority_score=1.0)

    greedy_res = GreedyAllocator().allocate([d], [a1, a2])
    fair_res = FairnessAwareAllocator().allocate([d], [a1, a2])

    # Greedy allocates all 100 to A1
    greedy_a1 = sum(item.allocated_quantity for item in greedy_res.allocations if item.agency_id == 'A1')
    greedy_a2 = sum(item.allocated_quantity for item in greedy_res.allocations if item.agency_id == 'A2')
    assert greedy_a1 == 100.0
    assert greedy_a2 == 0.0

    # Fair allocator distributes food to balance satisfaction ratios
    fair_a1 = sum(item.allocated_quantity for item in fair_res.allocations if item.agency_id == 'A1')
    fair_a2 = sum(item.allocated_quantity for item in fair_res.allocations if item.agency_id == 'A2')
    assert fair_a2 > 0.0
    assert fair_res.jain_fairness_index > greedy_res.jain_fairness_index


def test_determinism(base_location):
    donations = [
        Donation(id='D1', donor_id='DONOR1', food_type='produce', quantity=40.0, location=base_location),
        Donation(id='D2', donor_id='DONOR2', food_type='dairy', quantity=60.0, requires_refrigeration=True, location=base_location),
    ]
    agencies = [
        Agency(id='A1', name='Agency 1', location=base_location, storage_capacity=100.0, demands=50.0, refrigeration_capable=True),
        Agency(id='A2', name='Agency 2', location=base_location, storage_capacity=100.0, demands=50.0, refrigeration_capable=False),
    ]

    for allocator in [GreedyAllocator(), FairnessAwareAllocator()]:
        res1 = allocator.allocate(donations, agencies)
        res2 = allocator.allocate(donations, agencies)
        assert res1.total_allocated == res2.total_allocated
        assert [a.allocated_quantity for a in res1.allocations] == [a.allocated_quantity for a in res2.allocations]
