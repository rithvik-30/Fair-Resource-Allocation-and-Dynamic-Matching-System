from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.db.repositories.donors import DonorRepository
from backend.db.repositories.donations import DonationRepository
from backend.db.repositories.agencies import AgencyRepository
from backend.db.repositories.volunteers import VolunteerRepository
from backend.db.repositories.rescue_requests import RescueRequestRepository
from backend.db.repositories.records import ExecutionRepository
from backend.api.schemas.database import (
    DonorCreate, DonorRead,
    DonationCreate, DonationRead,
    AgencyCreate, AgencyRead,
    VolunteerCreate, VolunteerRead,
    RescueRequestCreate, RescueRequestRead,
    AllocationRecordCreate, AllocationRecordRead,
    DispatchRecordCreate, DispatchRecordRead
)

router = APIRouter(prefix="/api/v1", tags=["Database CRUD"])

# --- Donors ---
@router.post("/donors", response_model=DonorRead, status_code=status.HTTP_201_CREATED)
def create_donor_endpoint(donor: DonorCreate, db: Session = Depends(get_db)):
    repo = DonorRepository(db)
    return repo.create(donor)

@router.get("/donors", response_model=List[DonorRead])
def list_donors_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = DonorRepository(db)
    return repo.list_all(skip=skip, limit=limit)

@router.get("/donors/{donor_id}", response_model=DonorRead)
def get_donor_endpoint(donor_id: str, db: Session = Depends(get_db)):
    repo = DonorRepository(db)
    donor = repo.get_by_id(donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail=f"Donor {donor_id} not found")
    return donor

# --- Donations ---
@router.post("/donations", response_model=DonationRead, status_code=status.HTTP_201_CREATED)
def create_donation_endpoint(donation: DonationCreate, db: Session = Depends(get_db)):
    repo = DonationRepository(db)
    return repo.create(donation)

@router.get("/donations", response_model=List[DonationRead])
def list_donations_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = DonationRepository(db)
    return repo.list_all(skip=skip, limit=limit)

@router.get("/donations/{donation_id}", response_model=DonationRead)
def get_donation_endpoint(donation_id: str, db: Session = Depends(get_db)):
    repo = DonationRepository(db)
    donation = repo.get_by_id(donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail=f"Donation {donation_id} not found")
    return donation

# --- Agencies ---
@router.post("/agencies", response_model=AgencyRead, status_code=status.HTTP_201_CREATED)
def create_agency_endpoint(agency: AgencyCreate, db: Session = Depends(get_db)):
    repo = AgencyRepository(db)
    return repo.create(agency)

@router.get("/agencies", response_model=List[AgencyRead])
def list_agencies_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = AgencyRepository(db)
    return repo.list_all(skip=skip, limit=limit)

@router.get("/agencies/{agency_id}", response_model=AgencyRead)
def get_agency_endpoint(agency_id: str, db: Session = Depends(get_db)):
    repo = AgencyRepository(db)
    agency = repo.get_by_id(agency_id)
    if not agency:
        raise HTTPException(status_code=404, detail=f"Agency {agency_id} not found")
    return agency

# --- Volunteers ---
@router.post("/volunteers", response_model=VolunteerRead, status_code=status.HTTP_201_CREATED)
def create_volunteer_endpoint(volunteer: VolunteerCreate, db: Session = Depends(get_db)):
    repo = VolunteerRepository(db)
    return repo.create(volunteer)

@router.get("/volunteers", response_model=List[VolunteerRead])
def list_volunteers_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = VolunteerRepository(db)
    return repo.list_all(skip=skip, limit=limit)

@router.get("/volunteers/{volunteer_id}", response_model=VolunteerRead)
def get_volunteer_endpoint(volunteer_id: str, db: Session = Depends(get_db)):
    repo = VolunteerRepository(db)
    volunteer = repo.get_by_id(volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail=f"Volunteer {volunteer_id} not found")
    return volunteer

# --- Rescue Requests ---
@router.post("/rescue-requests", response_model=RescueRequestRead, status_code=status.HTTP_201_CREATED)
def create_rescue_request_endpoint(rr: RescueRequestCreate, db: Session = Depends(get_db)):
    repo = RescueRequestRepository(db)
    return repo.create(rr)

@router.get("/rescue-requests", response_model=List[RescueRequestRead])
def list_rescue_requests_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = RescueRequestRepository(db)
    return repo.list_all(skip=skip, limit=limit)

@router.get("/rescue-requests/{request_id}", response_model=RescueRequestRead)
def get_rescue_request_endpoint(request_id: str, db: Session = Depends(get_db)):
    repo = RescueRequestRepository(db)
    rr = repo.get_by_id(request_id)
    if not rr:
        raise HTTPException(status_code=404, detail=f"Rescue request {request_id} not found")
    return rr

# --- Execution Records ---
@router.get("/allocation-records", response_model=List[AllocationRecordRead])
def list_allocation_records_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = ExecutionRepository(db)
    return repo.list_allocations(skip=skip, limit=limit)

@router.get("/dispatch-records", response_model=List[DispatchRecordRead])
def list_dispatch_records_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = ExecutionRepository(db)
    return repo.list_dispatches(skip=skip, limit=limit)
