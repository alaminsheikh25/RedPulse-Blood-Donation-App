from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.core.enums import BloodGroup, InventoryStatus


class InventoryCreate(BaseModel):
    hospital_id: str
    blood_group: BloodGroup
    units_available: float = Field(default=0, ge=0)
    units_reserved: float = Field(default=0, ge=0)
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = None
    storage_location: Optional[str] = None


class InventoryUpdate(BaseModel):
    units_available: Optional[float] = Field(default=None, ge=0)
    units_reserved: Optional[float] = Field(default=None, ge=0)
    status: Optional[InventoryStatus] = None
    expiry_date: Optional[date] = None
    storage_location: Optional[str] = None


class InventoryResponse(BaseModel):
    id: str
    hospital_id: str
    blood_group: BloodGroup
    units_available: float
    units_reserved: float
    status: InventoryStatus
    expiry_date: Optional[date] = None
    batch_number: Optional[str] = None
    storage_location: Optional[str] = None

    model_config = {"from_attributes": True}
