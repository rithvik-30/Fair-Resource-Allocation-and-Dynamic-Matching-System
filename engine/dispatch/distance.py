import math
from engine.models.location import Location


def haversine_distance(location_a: Location, location_b: Location) -> float:
    """
    Calculate the Great-Circle distance between two geographical points using the Haversine formula.

    Formula:
        a = sin^2(dlat/2) + cos(lat1) * cos(lat2) * sin^2(dlon/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = R * c

    Assumptions:
        - Spherical Earth model with Mean Earth Radius R = 6371.0 km.
        - Latitudes in range [-90, 90] degrees, Longitudes in range [-180, 180] degrees.

    Time Complexity: O(1)
    Space Complexity: O(1)

    Args:
        location_a: Origin Location (latitude, longitude)
        location_b: Destination Location (latitude, longitude)

    Returns:
        Distance in kilometers (float)
    """
    return location_a.haversine_distance(location_b)
