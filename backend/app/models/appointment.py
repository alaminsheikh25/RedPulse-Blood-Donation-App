from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import AppointmentStatus
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    donor_id: Mapped[str] = mapped_column(String(36), ForeignKey("donors.id", ondelete="CASCADE"), nullable=False, index=True)
    hospital_id: Mapped[str] = mapped_column(String(36), ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False, index=True)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes: Mapped[int] = mapped_column(default=30, nullable=False)

    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus, name="appointment_status"), default=AppointmentStatus.PENDING, nullable=False, index=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    donor: Mapped["Donor"] = relationship(back_populates="appointments")
    hospital: Mapped["Hospital"] = relationship(back_populates="appointments")
    donation: Mapped[Optional["Donation"]] = relationship(back_populates="appointment", uselist=False)
