from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import BloodGroup, RequestStatus, RequestUrgency


class BloodRequestCreate(BaseModel):
    hospital_id: Optional[str] = None
    patient_name: Optional[str] = None
    patient_age: Optional[int] = Field(default=None, ge=0, le=120)
    blood_group: BloodGroup
    units_required: int = Field(gt=0, le=100)
    urgency: RequestUrgency = RequestUrgency.ROUTINE
    needed_by: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_description: Optional[str] = None
    notes: Optional[str] = None
    medical_notes: Optional[str] = None
    expires_at: Optional[datetime] = None


class BloodRequestUpdate(BaseModel):
    units_required: Optional[int] = Field(default=None, gt=0)
    urgency: Optional[RequestUrgency] = None
    status: Optional[RequestStatus] = None
    notes: Optional[str] = None


class BloodRequestResponse(BaseModel):
    id: str
    requester_user_id: str
    hospital_id: Optional[str] = None
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    blood_group: BloodGroup
    units_required: int
    units_fulfilled: int
    urgency: RequestUrgency
    status: RequestStatus
    needed_by: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_description: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
