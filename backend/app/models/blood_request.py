from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import BloodGroup, RequestStatus, RequestUrgency
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class BloodRequest(Base, TimestampMixin):
    __tablename__ = "blood_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    requester_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    hospital_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("hospitals.id", ondelete="SET NULL"), nullable=True, index=True)

    patient_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    patient_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    blood_group: Mapped[BloodGroup] = mapped_column(Enum(BloodGroup, name="blood_group"), nullable=False, index=True)
    units_required: Mapped[int] = mapped_column(Integer, nullable=False)
    units_fulfilled: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    urgency: Mapped[RequestUrgency] = mapped_column(Enum(RequestUrgency, name="request_urgency"), default=RequestUrgency.ROUTINE, nullable=False, index=True)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus, name="request_status"), default=RequestStatus.OPEN, nullable=False, index=True)

    needed_by: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    location_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    medical_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    hospital: Mapped[Optional["Hospital"]] = relationship(back_populates="requests")
    matches: Mapped[list["Match"]] = relationship(back_populates="request", cascade="all, delete-orphan")
    donations: Mapped[list["Donation"]] = relationship(back_populates="request")
