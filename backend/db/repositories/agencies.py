"""Agency repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models import AgencyModel
from backend.api.schemas.database import AgencyCreate


def create_agency(db: Session, agency: AgencyCreate) -> AgencyModel:
    db_agency = AgencyModel(
        name=agency.name,
        latitude=agency.latitude,
        longitude=agency.longitude,
        demand_kg=agency.demand_kg,
        storage_capacity_kg=agency.storage_capacity_kg,
        requires_refrigeration=agency.requires_refrigeration,
        priority=agency.priority,
    )
    db.add(db_agency)
    db.commit()
    db.refresh(db_agency)
    return db_agency


def get_agency(db: Session, agency_id: str) -> Optional[AgencyModel]:
    return db.query(AgencyModel).filter(AgencyModel.id == agency_id).first()


def list_agencies(db: Session, skip: int = 0, limit: int = 100) -> List[AgencyModel]:
    return db.query(AgencyModel).offset(skip).limit(limit).all()


class AgencyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, agency: AgencyCreate) -> AgencyModel:
        return create_agency(self.db, agency)

    def get_by_id(self, agency_id: str) -> Optional[AgencyModel]:
        return get_agency(self.db, agency_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[AgencyModel]:
        return list_agencies(self.db, skip=skip, limit=limit)
