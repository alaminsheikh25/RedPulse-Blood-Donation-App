from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import BloodGroup, Gender


class DonorCreate(BaseModel):
    blood_group: BloodGroup
    date_of_birth: date
    gender: Gender
    weight_kg: float = Field(gt=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    hemoglobin_g_dl: Optional[float] = None


class DonorUpdate(BaseModel):
    weight_kg: Optional[float] = Field(default=None, gt=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    hemoglobin_g_dl: Optional[float] = None
    is_available: Optional[bool] = None
    has_chronic_illness: Optional[bool] = None
    on_medication: Optional[bool] = None
    recent_tattoo_piercing: Optional[bool] = None
    recent_travel_risk: Optional[bool] = None
    notes: Optional[str] = None


class DonorResponse(BaseModel):
    id: str
    user_id: str
    blood_group: BloodGroup
    date_of_birth: date
    gender: Gender
    weight_kg: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    hemoglobin_g_dl: Optional[float] = None
    last_donation_date: Optional[date] = None
    total_donations: int
    is_available: bool
    is_eligible: bool
    deferred_until: Optional[date] = None
    reliability_score: float
    response_rate: float

    model_config = {"from_attributes": True}


class EligibilityResponse(BaseModel):
    eligible: bool
    reasons: list[str]
    next_eligible_date: Optional[date] = None
