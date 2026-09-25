import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.db.base import Base
from backend.db.session import get_db
from backend.main import app
from backend.db.models import (
    Donor, Donation, Agency, Volunteer, RescueRequest,
    AllocationRecord, DispatchRecord
)
from backend.db.repositories.donors import DonorRepository
from backend.db.repositories.donations import DonationRepository
from backend.db.repositories.agencies import AgencyRepository
from backend.db.repositories.volunteers import VolunteerRepository
from backend.db.repositories.rescue_requests import RescueRequestRepository
from backend.db.repositories.records import ExecutionRecordRepository
from backend.api.schemas.database import (
    DonorCreate, DonationCreate, AgencyCreate, VolunteerCreate, RescueRequestCreate
)

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_sqlalchemy_models_importable():
    assert Donor is not None
    assert Donation is not None
    assert Agency is not None
    assert Volunteer is not None
    assert RescueRequest is not None
    assert AllocationRecord is not None
    assert DispatchRecord is not None

def test_repositories_crud(db_session):
    donor_repo = DonorRepository(db_session)
    donation_repo = DonationRepository(db_session)
    agency_repo = AgencyRepository(db_session)
    vol_repo = VolunteerRepository(db_session)
    rr_repo = RescueRequestRepository(db_session)
    rec_repo = ExecutionRecordRepository(db_session)

    # 1. Create Donor
    donor = donor_repo.create(DonorCreate(name="Test Donor", latitude=37.77, longitude=-122.41))
    assert donor.id is not None
    assert donor_repo.get_by_id(donor.id).name == "Test Donor"

    # 2. Create Donation
    now = datetime.now(timezone.utc)
    donation = donation_repo.create(DonationCreate(
        donor_id=donor.id,
        food_type="Prepared Meals",
        quantity_kg=100.0,
        available_from=now,
        available_until=now,
        requires_refrigeration=False
    ))
    assert donation.id is not None

    # 3. Create Agency
    agency = agency_repo.create(AgencyCreate(
        name="Test Shelter",
        latitude=37.78,
        longitude=-122.42,
        demand_kg=50.0,
        storage_capacity_kg=200.0,
        requires_refrigeration=False,
        priority=3
    ))
    assert agency.id is not None

    # 4. Create Volunteer
    vol = vol_repo.create(VolunteerCreate(
        name="Test Volunteer",
        latitude=37.76,
        longitude=-122.40,
        capacity_kg=60.0,
        has_refrigeration=True,
        available_from=now,
        available_until=now,
        current_workload_kg=0.0,
        max_travel_distance_km=15.0
    ))
    assert vol.id is not None

    # 5. Create RescueRequest
    rr = rr_repo.create(RescueRequestCreate(
        donation_id=donation.id,
        agency_id=agency.id,
        requested_quantity_kg=50.0,
        pickup_deadline=now,
        status="pending"
    ))
    assert rr.id is not None

    # 6. Create Execution Records
    alloc_rec = rec_repo.create_allocation(
        donation_id=donation.id,
        agency_id=agency.id,
        quantity_kg=50.0,
        algorithm="GreedyAllocator"
    )
    assert alloc_rec.id is not None

    disp_rec = rec_repo.create_dispatch(
        rescue_request_id=rr.id,
        volunteer_id=vol.id,
        algorithm="NearestVolunteerDispatcher",
        distance_km=2.5
    )
    assert disp_rec.id is not None

def test_database_health_endpoint(client):
    res = client.get("/api/v1/database/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["database"] == "postgresql"

def test_crud_api_endpoints(client):
    # Donor API
    res = client.post("/api/v1/donors", json={
        "name": "API Donor",
        "latitude": 40.71,
        "longitude": -74.00
    })
    assert res.status_code == 201
    donor_id = res.json()["id"]

    res_list = client.get("/api/v1/donors")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    res_get = client.get(f"/api/v1/donors/{donor_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == donor_id
