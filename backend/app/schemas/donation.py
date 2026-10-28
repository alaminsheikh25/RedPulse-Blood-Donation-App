from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import DonationStatus, DonationType


class DonationCreate(BaseModel):
    hospital_id: Optional[str] = None
    request_id: Optional[str] = None
    appointment_id: Optional[str] = None
    donation_type: DonationType = DonationType.WHOLE_BLOOD
    scheduled_date: Optional[date] = None
    units: float = Field(default=1.0, gt=0)


class DonationUpdate(BaseModel):
    status: Optional[DonationStatus] = None
    donation_date: Optional[date] = None
    hemoglobin_before: Optional[float] = None
    blood_pressure: Optional[str] = None
    pulse: Optional[int] = None
    weight_at_donation: Optional[float] = None
    temperature_c: Optional[float] = None
    notes: Optional[str] = None
    deferral_reason: Optional[str] = None


class DonationResponse(BaseModel):
    id: str
    donor_id: str
    hospital_id: Optional[str] = None
    request_id: Optional[str] = None
    donation_type: DonationType
    status: DonationStatus
    scheduled_date: Optional[date] = None
    donation_date: Optional[date] = None
    units: float
    created_at: date

    model_config = {"from_attributes": True}
