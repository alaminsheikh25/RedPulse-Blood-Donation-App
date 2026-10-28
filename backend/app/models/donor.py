from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import BloodGroup, Gender
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class Donor(Base, TimestampMixin):
    __tablename__ = "donors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    blood_group: Mapped[BloodGroup] = mapped_column(Enum(BloodGroup, name="blood_group"), nullable=False, index=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender, name="gender"), nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)

    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, index=True)
    state: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    hemoglobin_g_dl: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_donation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    total_donations: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_eligible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    deferred_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    has_chronic_illness: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    on_medication: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recent_tattoo_piercing: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recent_travel_risk: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reliability_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    response_rate: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    user: Mapped["User"] = relationship(back_populates="donor_profile")
    donations: Mapped[list["Donation"]] = relationship(back_populates="donor", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="donor", cascade="all, delete-orphan")
    matches: Mapped[list["Match"]] = relationship(back_populates="donor", cascade="all, delete-orphan")

    def age(self, as_of: Optional[date] = None) -> int:
        as_of = as_of or date.today()
        born = self.date_of_birth
        years = as_of.year - born.year
        if (as_of.month, as_of.day) < (born.month, born.day):
            years -= 1
        return years
