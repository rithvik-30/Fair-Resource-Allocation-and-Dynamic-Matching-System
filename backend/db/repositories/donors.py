"""Donor repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models import DonorModel
from backend.api.schemas.database import DonorCreate


def create_donor(db: Session, donor: DonorCreate) -> DonorModel:
    db_donor = DonorModel(
        name=donor.name,
        latitude=donor.latitude,
        longitude=donor.longitude,
    )
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor


def get_donor(db: Session, donor_id: str) -> Optional[DonorModel]:
    return db.query(DonorModel).filter(DonorModel.id == donor_id).first()


def list_donors(db: Session, skip: int = 0, limit: int = 100) -> List[DonorModel]:
    return db.query(DonorModel).offset(skip).limit(limit).all()


class DonorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donor: DonorCreate) -> DonorModel:
        return create_donor(self.db, donor)

    def get_by_id(self, donor_id: str) -> Optional[DonorModel]:
        return get_donor(self.db, donor_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[DonorModel]:
        return list_donors(self.db, skip=skip, limit=limit)
