from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import DonationStatus, DonationType
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class Donation(Base, TimestampMixin):
    __tablename__ = "donations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    donor_id: Mapped[str] = mapped_column(String(36), ForeignKey("donors.id", ondelete="CASCADE"), nullable=False, index=True)
    hospital_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("hospitals.id", ondelete="SET NULL"), nullable=True, index=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("blood_requests.id", ondelete="SET NULL"), nullable=True, index=True)
    appointment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("appointments.id", ondelete="SET NULL"), nullable=True)

    donation_type: Mapped[DonationType] = mapped_column(Enum(DonationType, name="donation_type"), default=DonationType.WHOLE_BLOOD, nullable=False)
    status: Mapped[DonationStatus] = mapped_column(Enum(DonationStatus, name="donation_status"), default=DonationStatus.SCHEDULED, nullable=False, index=True)

    scheduled_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    donation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    units: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    hemoglobin_before: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    blood_pressure: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    pulse: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight_at_donation: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    temperature_c: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    deferral_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    donor: Mapped["Donor"] = relationship(back_populates="donations")
    hospital: Mapped[Optional["Hospital"]] = relationship(back_populates="donations")
    request: Mapped[Optional["BloodRequest"]] = relationship(back_populates="donations")
    appointment: Mapped[Optional["Appointment"]] = relationship(back_populates="donation")
    inventory_items: Mapped[list["Inventory"]] = relationship(back_populates="source_donation")
