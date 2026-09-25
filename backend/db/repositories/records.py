"""Execution records repository."""

from typing import List
from sqlalchemy.orm import Session
from backend.db.models import AllocationRecordModel, DispatchRecordModel


def create_allocation_record(
    db: Session,
    donation_id: str,
    agency_id: str,
    quantity_kg: float,
    algorithm: str,
) -> AllocationRecordModel:
    record = AllocationRecordModel(
        donation_id=donation_id,
        agency_id=agency_id,
        quantity_kg=quantity_kg,
        algorithm=algorithm,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_allocation_records(
    db: Session, skip: int = 0, limit: int = 100
) -> List[AllocationRecordModel]:
    return db.query(AllocationRecordModel).offset(skip).limit(limit).all()


def create_dispatch_record(
    db: Session,
    rescue_request_id: str,
    volunteer_id: str,
    algorithm: str,
    distance_km: float,
) -> DispatchRecordModel:
    record = DispatchRecordModel(
        rescue_request_id=rescue_request_id,
        volunteer_id=volunteer_id,
        algorithm=algorithm,
        distance_km=distance_km,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_dispatch_records(
    db: Session, skip: int = 0, limit: int = 100
) -> List[DispatchRecordModel]:
    return db.query(DispatchRecordModel).offset(skip).limit(limit).all()


class ExecutionRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_allocation(self, donation_id: str, agency_id: str, quantity_kg: float, algorithm: str) -> AllocationRecordModel:
        return create_allocation_record(self.db, donation_id, agency_id, quantity_kg, algorithm)

    def list_allocations(self, skip: int = 0, limit: int = 100) -> List[AllocationRecordModel]:
        return list_allocation_records(self.db, skip=skip, limit=limit)

    def create_dispatch(self, rescue_request_id: str, volunteer_id: str, algorithm: str, distance_km: float) -> DispatchRecordModel:
        return create_dispatch_record(self.db, rescue_request_id, volunteer_id, algorithm, distance_km)

    def list_dispatches(self, skip: int = 0, limit: int = 100) -> List[DispatchRecordModel]:
        return list_dispatch_records(self.db, skip=skip, limit=limit)

ExecutionRepository = ExecutionRecordRepository
