import pytest
from engine.metrics.fairness import (
    allocation_disparity,
    compute_allocation_ratios,
    jains_fairness_index,
)
from engine.models.agency import Agency
from engine.models.allocation_result import AllocationResult
from engine.models.location import Location


def test_jains_fairness_index_equal():
    ratios = [0.5, 0.5, 0.5, 0.5]
    assert jains_fairness_index(ratios) == 1.0


def test_jains_fairness_index_unequal():
    ratios = [1.0, 0.0]
    assert jains_fairness_index(ratios) == pytest.approx(0.5)


def test_jains_fairness_index_edge_cases():
    assert jains_fairness_index([]) == 1.0
    assert jains_fairness_index([0.0, 0.0, 0.0]) == 1.0


def test_allocation_disparity():
    ratios = {'A1': 0.8, 'A2': 0.2, 'A3': 0.5}
    assert allocation_disparity(ratios) == pytest.approx(0.6)
    assert allocation_disparity([]) == 0.0


def test_compute_allocation_ratios():
    loc = Location(latitude=0.0, longitude=0.0)
    a1 = Agency(
        id='A1',
        name='Agency 1',
        location=loc,
        storage_capacity=100.0,
        demands=100.0,
        historical_allocations=10.0,
    )
    a2 = Agency(
        id='A2',
        name='Agency 2',
        location=loc,
        storage_capacity=100.0,
        demands=50.0,
        historical_allocations=0.0,
    )

    allocs = [
        AllocationResult(donation_id='D1', agency_id='A1', allocated_quantity=40.0),
        AllocationResult(donation_id='D1', agency_id='A2', allocated_quantity=25.0),
    ]

    ratios = compute_allocation_ratios([a1, a2], allocs)
    assert ratios['A1'] == pytest.approx(0.5)
    assert ratios['A2'] == pytest.approx(0.5)
