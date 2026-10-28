from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import MatchStatus
from app.database import Base
from app.models.user import TimestampMixin, new_uuid


class Match(Base, TimestampMixin):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    request_id: Mapped[str] = mapped_column(String(36), ForeignKey("blood_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    donor_id: Mapped[str] = mapped_column(String(36), ForeignKey("donors.id", ondelete="CASCADE"), nullable=False, index=True)

    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    distance_km: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus, name="match_status"), default=MatchStatus.PENDING, nullable=False, index=True)

    contacted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    response_note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    request: Mapped["BloodRequest"] = relationship(back_populates="matches")
    donor: Mapped["Donor"] = relationship(back_populates="matches")
