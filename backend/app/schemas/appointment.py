from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import AppointmentStatus


class AppointmentCreate(BaseModel):
    hospital_id: str
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, gt=0, le=240)
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    cancellation_reason: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: str
    donor_id: str
    hospital_id: str
    scheduled_at: datetime
    duration_minutes: int
    status: AppointmentStatus
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
