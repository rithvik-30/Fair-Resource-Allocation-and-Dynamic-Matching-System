from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from engine.models.agency import Agency
from engine.models.donation import Donation
from engine.models.rescue_request import RescueRequest
from engine.models.volunteer import Volunteer
from simulation.generators.allocation_data import generate_allocation_scenario
from simulation.generators.dispatch_data import generate_dispatch_scenario


@dataclass
class AllocationScenario:
    problem_size: int
    donations: List[Donation]
    agencies: List[Agency]
    seed: int
    total_supply: float
    total_demand: float


@dataclass
class DispatchScenario:
    problem_size: int
    requests: List[RescueRequest]
    volunteers: List[Volunteer]
    seed: int
    num_requests: int
    num_volunteers: int


def build_allocation_scenario(
    num_donations: int,
    num_agencies: int,
    seed: int = 42,
) -> AllocationScenario:
    donations, agencies = generate_allocation_scenario(
        num_donations=num_donations,
        num_agencies=num_agencies,
        seed=seed,
    )
    total_supply = sum(d.quantity for d in donations)
    total_demand = sum(a.demands for a in agencies)
    problem_size = num_donations

    return AllocationScenario(
        problem_size=problem_size,
        donations=donations,
        agencies=agencies,
        seed=seed,
        total_supply=total_supply,
        total_demand=total_demand,
    )


def build_dispatch_scenario(
    num_requests: int,
    num_volunteers: int,
    seed: int = 42,
) -> DispatchScenario:
    requests, volunteers = generate_dispatch_scenario(
        num_requests=num_requests,
        num_volunteers=num_volunteers,
        seed=seed,
    )
    problem_size = num_requests

    return DispatchScenario(
        problem_size=problem_size,
        requests=requests,
        volunteers=volunteers,
        seed=seed,
        num_requests=num_requests,
        num_volunteers=num_volunteers,
    )
