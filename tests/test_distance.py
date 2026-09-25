import math
from engine.dispatch.distance import haversine_distance
from engine.models.location import Location


def test_haversine_identical_locations():
    loc = Location(latitude=40.7128, longitude=-74.0060)
    assert haversine_distance(loc, loc) == 0.0


def test_haversine_symmetry():
    loc_a = Location(latitude=40.7128, longitude=-74.0060)
    loc_b = Location(latitude=34.0522, longitude=-118.2437)
    dist_a_b = haversine_distance(loc_a, loc_b)
    dist_b_a = haversine_distance(loc_b, loc_a)
    assert math.isclose(dist_a_b, dist_b_a, rel_tol=1e-6)
    assert 3900 < dist_a_b < 4000


def test_haversine_known_distance():
    london = Location(latitude=51.5074, longitude=-0.1278)
    paris = Location(latitude=48.8566, longitude=2.3522)
    dist = haversine_distance(london, paris)
    assert 340.0 <= dist <= 350.0
