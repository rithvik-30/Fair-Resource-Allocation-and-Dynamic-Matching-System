"""Rescue request repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.db.models import RescueRequestModel
from backend.api.schemas.database import RescueRequestCreate


def create_rescue_request(db: Session, request: RescueRequestCreate) -> RescueRequestModel:
    db_request = RescueRequestModel(
        donation_id=request.donation_id,
        agency_id=request.agency_id,
        requested_quantity_kg=request.requested_quantity_kg,
        pickup_deadline=request.pickup_deadline,
        status=request.status or "pending",
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_rescue_request(db: Session, request_id: str) -> Optional[RescueRequestModel]:
    return db.query(RescueRequestModel).filter(RescueRequestModel.id == request_id).first()


def list_rescue_requests(db: Session, skip: int = 0, limit: int = 100) -> List[RescueRequestModel]:
    return db.query(RescueRequestModel).offset(skip).limit(limit).all()


class RescueRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, request: RescueRequestCreate) -> RescueRequestModel:
        return create_rescue_request(self.db, request)

    def get_by_id(self, request_id: str) -> Optional[RescueRequestModel]:
        return get_rescue_request(self.db, request_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> List[RescueRequestModel]:
        return list_rescue_requests(self.db, skip=skip, limit=limit)
