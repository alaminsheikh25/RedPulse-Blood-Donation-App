from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import BloodGroup, InventoryStatus
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    hospital_id: Mapped[str] = mapped_column(String(36), ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False, index=True)
    blood_group: Mapped[BloodGroup] = mapped_column(Enum(BloodGroup, name="blood_group"), nullable=False, index=True)

    units_available: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    units_reserved: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    status: Mapped[InventoryStatus] = mapped_column(Enum(InventoryStatus, name="inventory_status"), default=InventoryStatus.AVAILABLE, nullable=False)

    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    batch_number: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    storage_location: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    source_donation_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("donations.id", ondelete="SET NULL"), nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    hospital: Mapped["Hospital"] = relationship(back_populates="inventory")
    source_donation: Mapped[Optional["Donation"]] = relationship(back_populates="inventory_items")
