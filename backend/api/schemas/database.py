from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Union
from datetime import datetime

# Donor Schemas
class DonorBase(BaseModel):
    name: str = Field(..., json_schema_extra={'example': 'Central Food Bank'})
    organization_type: Optional[str] = Field(None, json_schema_extra={'example': 'Non-Profit'})
    latitude: float = Field(..., json_schema_extra={'example': 37.7749})
    longitude: float = Field(..., json_schema_extra={'example': -122.4194})

class DonorCreate(DonorBase):
    id: Optional[Union[str, int]] = None

class DonorResponse(DonorBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Donation Schemas
class DonationBase(BaseModel):
    donor_id: Union[str, int] = Field(..., json_schema_extra={'example': 'donor_1'})
    food_type: str = Field(..., json_schema_extra={'example': 'Prepared Meals'})
    quantity_kg: float = Field(..., gt=0, json_schema_extra={'example': 150.0})
    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None
    requires_refrigeration: bool = False

class DonationCreate(DonationBase):
    id: Optional[Union[str, int]] = None

class DonationResponse(DonationBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Agency Schemas
class AgencyBase(BaseModel):
    name: str = Field(..., json_schema_extra={'example': 'Hope Shelter'})
    latitude: float = Field(..., json_schema_extra={'example': 37.7833})
    longitude: float = Field(..., json_schema_extra={'example': -122.4167})
    demand_kg: float = Field(..., ge=0, json_schema_extra={'example': 80.0})
    storage_capacity_kg: float = Field(..., gt=0, json_schema_extra={'example': 200.0})
    requires_refrigeration: bool = False
    priority: int = Field(1, ge=1, le=5, json_schema_extra={'example': 2})

class AgencyCreate(AgencyBase):
    id: Optional[Union[str, int]] = None

class AgencyResponse(AgencyBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Volunteer Schemas
class VolunteerBase(BaseModel):
    name: str = Field(..., json_schema_extra={'example': 'Alex Rivers'})
    latitude: float = Field(..., json_schema_extra={'example': 37.7750})
    longitude: float = Field(..., json_schema_extra={'example': -122.4180})
    capacity_kg: float = Field(..., gt=0, json_schema_extra={'example': 50.0})
    has_refrigeration: bool = False
    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None
    current_workload_kg: float = Field(0.0, ge=0)
    max_travel_distance_km: float = Field(15.0, gt=0)

class VolunteerCreate(VolunteerBase):
    id: Optional[Union[str, int]] = None

class VolunteerResponse(VolunteerBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# RescueRequest Schemas
class RescueRequestBase(BaseModel):
    donation_id: Union[str, int]
    agency_id: Union[str, int]
    requested_quantity_kg: float = Field(..., gt=0)
    pickup_deadline: Optional[datetime] = None
    status: str = Field('pending', json_schema_extra={'example': 'pending'})

class RescueRequestCreate(RescueRequestBase):
    id: Optional[Union[str, int]] = None

class RescueRequestResponse(RescueRequestBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# AllocationRecord Schemas
class AllocationRecordBase(BaseModel):
    donation_id: Union[str, int]
    agency_id: Union[str, int]
    quantity_kg: float
    algorithm: str

class AllocationRecordCreate(AllocationRecordBase):
    id: Optional[Union[str, int]] = None

class AllocationRecordResponse(AllocationRecordBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# DispatchRecord Schemas
class DispatchRecordBase(BaseModel):
    rescue_request_id: Union[str, int]
    volunteer_id: Union[str, int]
    algorithm: str
    distance_km: float

class DispatchRecordCreate(DispatchRecordBase):
    id: Optional[Union[str, int]] = None

class DispatchRecordResponse(DispatchRecordBase):
    id: Union[str, int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Health Response
class DatabaseHealthResponse(BaseModel):
    status: str = Field('ok', json_schema_extra={'example': 'ok'})
    database: str = Field('postgresql', json_schema_extra={'example': 'postgresql'})

# Aliases for Read/Response compatibility
DonorRead = DonorResponse
DonationRead = DonationResponse
AgencyRead = AgencyResponse
VolunteerRead = VolunteerResponse
RescueRequestRead = RescueRequestResponse
AllocationRecordRead = AllocationRecordResponse
DispatchRecordRead = DispatchRecordResponse
