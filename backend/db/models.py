"""SQLAlchemy ORM models for FRADMS database entities."""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db.base import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DonorModel(Base):
    __tablename__ = "donors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    donations: Mapped[list["DonationModel"]] = relationship("DonationModel", back_populates="donor", cascade="all, delete-orphan")


class DonationModel(Base):
    __tablename__ = "donations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    donor_id: Mapped[str] = mapped_column(String(36), ForeignKey("donors.id", ondelete="CASCADE"), nullable=False, index=True)
    food_type: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    available_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    available_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    requires_refrigeration: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    donor: Mapped["DonorModel"] = relationship("DonorModel", back_populates="donations")
    rescue_requests: Mapped[list["RescueRequestModel"]] = relationship("RescueRequestModel", back_populates="donation", cascade="all, delete-orphan")
    allocations: Mapped[list["AllocationRecordModel"]] = relationship("AllocationRecordModel", back_populates="donation", cascade="all, delete-orphan")


class AgencyModel(Base):
    __tablename__ = "agencies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    demand_kg: Mapped[float] = mapped_column(Float, nullable=False)
    storage_capacity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    requires_refrigeration: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    rescue_requests: Mapped[list["RescueRequestModel"]] = relationship("RescueRequestModel", back_populates="agency", cascade="all, delete-orphan")
    allocations: Mapped[list["AllocationRecordModel"]] = relationship("AllocationRecordModel", back_populates="agency", cascade="all, delete-orphan")


class VolunteerModel(Base):
    __tablename__ = "volunteers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    capacity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    has_refrigeration: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    available_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    available_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    current_workload_kg: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    max_travel_distance_km: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    dispatches: Mapped[list["DispatchRecordModel"]] = relationship("DispatchRecordModel", back_populates="volunteer", cascade="all, delete-orphan")


class RescueRequestModel(Base):
    __tablename__ = "rescue_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    donation_id: Mapped[str] = mapped_column(String(36), ForeignKey("donations.id", ondelete="CASCADE"), nullable=False, index=True)
    agency_id: Mapped[str] = mapped_column(String(36), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_quantity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    pickup_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    donation: Mapped["DonationModel"] = relationship("DonationModel", back_populates="rescue_requests")
    agency: Mapped["AgencyModel"] = relationship("AgencyModel", back_populates="rescue_requests")
    dispatches: Mapped[list["DispatchRecordModel"]] = relationship("DispatchRecordModel", back_populates="rescue_request", cascade="all, delete-orphan")


class AllocationRecordModel(Base):
    __tablename__ = "allocation_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    donation_id: Mapped[str] = mapped_column(String(36), ForeignKey("donations.id", ondelete="CASCADE"), nullable=False, index=True)
    agency_id: Mapped[str] = mapped_column(String(36), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    algorithm: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    donation: Mapped["DonationModel"] = relationship("DonationModel", back_populates="allocations")
    agency: Mapped["AgencyModel"] = relationship("AgencyModel", back_populates="allocations")


class DispatchRecordModel(Base):
    __tablename__ = "dispatch_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    rescue_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("rescue_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    volunteer_id: Mapped[str] = mapped_column(String(36), ForeignKey("volunteers.id", ondelete="CASCADE"), nullable=False, index=True)
    algorithm: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, index=True)

    rescue_request: Mapped["RescueRequestModel"] = relationship("RescueRequestModel", back_populates="dispatches")
    volunteer: Mapped["VolunteerModel"] = relationship("VolunteerModel", back_populates="dispatches")


Donor = DonorModel
Donation = DonationModel
Agency = AgencyModel
Volunteer = VolunteerModel
RescueRequest = RescueRequestModel
AllocationRecord = AllocationRecordModel
DispatchRecord = DispatchRecordModel
