"""Donation repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models import DonationModel
from backend.api.schemas.database import DonationCreate


def create_donation(db: Session, donation: DonationCreate) -> DonationModel:
    db_donation = DonationModel(
        donor_id=donation.donor_id,
        food_type=donation.food_type,
        quantity_kg=donation.quantity_kg,
        available_from=donation.available_from,
        available_until=donation.available_until,
        requires_refrigeration=donation.requires_refrigeration,
    )
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation


def get_donation(db: Session, donation_id: str) -> Optional[DonationModel]:
    return db.query(DonationModel).filter(DonationModel.id == donation_id).first()


def list_donations(db: Session, skip: int = 0, limit: int = 100) -> List[DonationModel]:
    return db.query(DonationModel).offset(skip).limit(limit).all()


class DonationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donation: DonationCreate) -> DonationModel:
        return create_donation(self.db, donation)

    def get_by_id(self, donation_id: str) -> Optional[DonationModel]:
        return get_donation(self.db, donation_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[DonationModel]:
        return list_donations(self.db, skip=skip, limit=limit)
