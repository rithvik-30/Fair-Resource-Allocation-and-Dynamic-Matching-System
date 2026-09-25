import math
from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    """Geographical coordinate representation (latitude, longitude)."""

    latitude: float = Field(..., description="Latitude in degrees (-90 to 90)")
    longitude: float = Field(..., description="Longitude in degrees (-180 to 180)")

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not (-90.0 <= v <= 90.0):
            raise ValueError(
                f"Latitude must be between -90 and 90 degrees, got {v}"
            )
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not (-180.0 <= v <= 180.0):
            raise ValueError(
                f"Long itude must be between -180 and 180 degrees, got {v}"
            )
        return v

    def haversine_distance(self, other: "Location") -> float:
        """Calculate the Great,Circle (Haversine) distance to another location in kilometers."""
        R = 6371.0  # Earth radius in km

        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
