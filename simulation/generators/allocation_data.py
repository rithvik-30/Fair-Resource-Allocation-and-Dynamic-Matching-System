from datetime import datetime, timezone
import random
from typing import List, Optional, Tuple

from engine.models.agency import Agency
from engine.models.donation import Donation
from simulation.generators.locations import DEFAULT_BOUNDING_BOX, generate_locations


def generate_allocation_scenario(
    num_donations: int,
    num_agencies: int,
    seed: Optional[int] = 42,
    bounding_box: Tuple[float, float, float, float] = DEFAULT_BOUNDING_BOX,
    base_time: Optional[datetime] = None,
) -> Tuple[List[Donation], List[Agency]]:
    """Generates synthetic Donations and Agencies for allocation benchmarks.

    Completely deterministic given the same seed.
    Includes realistic variation in agency demand, priorities, capacities, and history.
    """
    rng = random.Random(seed)
    if base_time is None:
        base_time = datetime(2026, 9, 25, 10, 0, 0, tzinfo=timezone.utc)

    donor_locs = generate_locations(num_donations, bounding_box, seed=rng.randint(0, 2**31 - 1))
    agency_locs = generate_locations(num_agencies, bounding_box, seed=rng.randint(0, 2**31 - 1))

    food_types = ["Produce", "Dairy", "Prepared Meals", "Bakery", "Canned Goods"]

    donations: List[Donation] = []
    for i in range(num_donations):
        d_seed = rng.randint(0, 2**31 - 1)
        d_rng = random.Random(d_seed)

        qty = round(d_rng.uniform(20.0, 500.0), 1)
        requires_refrig = d_rng.random() < 0.3
        food_choice = d_rng.choice(food_types)

        donation = Donation(
            id=f"DONATION_{i + 1:04d}",
            donor_id=f"DONOR_{d_rng.randint(1, 20):03d}",
            food_type=food_choice,
            quantity=qty,
            perishable=True,
            expiration_hours=round(d_rng.uniform(6.0, 72.0), 1),
            requires_refrigeration=requires_refrig,
            created_at=base_time,
            location=donor_locs[i],
        )
        donations.append(donation)

    agencies: List[Agency] = []
    for j in range(num_agencies):
        a_seed = rng.randint(0, 2**31 - 1)
        a_rng = random.Random(a_seed)

        demand = round(a_rng.uniform(50.0, 800.0), 1)
        capacity = round(demand * a_rng.uniform(0.8, 2.0), 1)
        priority = float(a_rng.randint(1, 5))
        has_refrig = a_rng.random() < 0.5
        history = round(a_rng.uniform(0.0, 1500.0), 1)

        agency = Agency(
            id=f"AGENCY_{j + 1:04d}",
            name=f"Agency_{j + 1:04d}",
            location=agency_locs[j],
            storage_capacity=capacity,
            current_inventory=0.0,
            demands=demand,
            priority_score=priority,
            historical_allocations=history,
            refrigeration_capable=has_refrig,
        )
        agencies.append(agency)

    return donations, agencies
