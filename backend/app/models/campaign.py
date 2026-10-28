from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import CampaignStatus
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class Campaign(Base, TimestampMixin):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    hospital_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("hospitals.id", ondelete="SET NULL"), nullable=True, index=True)
    organizer_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    target_blood_groups: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    target_units: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    collected_units: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    status: Mapped[CampaignStatus] = mapped_column(Enum(CampaignStatus, name="campaign_status"), default=CampaignStatus.DRAFT, nullable=False, index=True)

    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    hospital: Mapped[Optional["Hospital"]] = relationship(back_populates="campaigns")
