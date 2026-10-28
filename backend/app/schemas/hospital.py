from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class HospitalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    registration_number: Optional[str] = None
    address: str
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "India"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    has_blood_bank: bool = False


class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    has_blood_bank: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None


class HospitalResponse(BaseModel):
    id: str
    name: str
    registration_number: Optional[str] = None
    address: str
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    has_blood_bank: bool
    is_verified: bool
    is_active: bool

    model_config = {"from_attributes": True}
