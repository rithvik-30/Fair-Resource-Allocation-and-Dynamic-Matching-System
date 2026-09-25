"""Volunteer repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models import VolunteerModel
from backend.api.schemas.database import VolunteerCreate


def create_volunteer(db: Session, volunteer: VolunteerCreate) -> VolunteerModel:
    db_volunteer = VolunteerModel(
        name=volunteer.name,
        latitude=volunteer.latitude,
        longitude=volunteer.longitude,
        capacity_kg=volunteer.capacity_kg,
        has_refrigeration=volunteer.has_refrigeration,
        available_from=volunteer.available_from,
        available_until=volunteer.available_until,
        current_workload_kg=volunteer.current_workload_kg,
        max_travel_distance_km=volunteer.max_travel_distance_km,
    )
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer


def get_volunteer(db: Session, volunteer_id: str) -> Optional[VolunteerModel]:
    return db.query(VolunteerModel).filter(VolunteerModel.id == volunteer_id).first()


def list_volunteers(db: Session, skip: int = 0, limit: int = 100) -> List[VolunteerModel]:
    return db.query(VolunteerModel).offset(skip).limit(limit).all()


class VolunteerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, volunteer: VolunteerCreate) -> VolunteerModel:
        return create_volunteer(self.db, volunteer)

    def get_by_id(self, volunteer_id: str) -> Optional[VolunteerModel]:
        return get_volunteer(self.db, volunteer_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[VolunteerModel]:
        return list_volunteers(self.db, skip=skip, limit=limit)
