from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.appointment import Appointment
from app.models.donor import Donor
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    payload: AppointmentCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Appointment:
    result = await db.execute(select(Donor).where(Donor.user_id == current_user.id))
    donor = result.scalar_one_or_none()
    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donor profile required")
    appt = Appointment(donor_id=donor.id, **payload.model_dump())
    db.add(appt)
    await db.flush()
    await db.refresh(appt)
    return appt


@router.get("", response_model=list[AppointmentResponse])
async def list_appointments(db: AsyncSession = Depends(get_db)) -> list[Appointment]:
    result = await db.execute(select(Appointment).order_by(Appointment.scheduled_at))
    return list(result.scalars().all())


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: str,
    payload: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
) -> Appointment:
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appt = result.scalar_one_or_none()
    if appt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(appt, field, value)
    await db.flush()
    await db.refresh(appt)
    return appt
