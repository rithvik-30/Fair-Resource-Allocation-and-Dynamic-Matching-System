import random
from typing import List, Optional, Tuple

from engine.models.location import Location

# Default bounding box for San Francisco region (min_lat, max_lat, min_lon, max_lon)
DEFAULT_BOUNDING_BOX: Tuple[float, float, float, float] = (37.70, 37.85, -122.52, -122.35)


def generate_locations(
    count: int,
    bounding_box: Tuple[float, float, float, float] = DEFAULT_BOUNDING_BOX,
    seed: Optional[int] = 42,
) -> List[Location]:
    """Generates synthetic lat/lon locations inside a bounding box deterministically.

    NOTE: All generated geographic coordinates are SYNTHETIC benchmark data
    and are not real operational locations.
    """
    rng = random.Random(seed)
    min_lat, max_lat, min_lon, max_lon = bounding_box

    locations: List[Location] = []
    for _ in range(count):
        lat = round(rng.uniform(min_lat, max_lat), 6)
        lon = round(rng.uniform(min_lon, max_lon), 6)
        locations.append(Location(latitude=lat, longitude=lon))

    return locations
