from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.database import get_db
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalResponse, HospitalUpdate

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.post("", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    payload: HospitalCreate,
    current_user=Depends(require_roles("admin", "super_admin", "hospital_staff")),
    db: AsyncSession = Depends(get_db),
) -> Hospital:
    hospital = Hospital(**payload.model_dump())
    db.add(hospital)
    await db.flush()
    await db.refresh(hospital)
    return hospital


@router.get("", response_model=list[HospitalResponse])
async def list_hospitals(city: str | None = None, db: AsyncSession = Depends(get_db)) -> list[Hospital]:
    stmt = select(Hospital).where(Hospital.is_active.is_(True))
    if city:
        stmt = stmt.where(Hospital.city.ilike(f"%{city}%"))
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(hospital_id: str, db: AsyncSession = Depends(get_db)) -> Hospital:
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalar_one_or_none()
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    return hospital


@router.patch("/{hospital_id}", response_model=HospitalResponse)
async def update_hospital(
    hospital_id: str,
    payload: HospitalUpdate,
    current_user=Depends(require_roles("admin", "super_admin", "hospital_staff")),
    db: AsyncSession = Depends(get_db),
) -> Hospital:
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalar_one_or_none()
    if hospital is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(hospital, field, value)
    await db.flush()
    await db.refresh(hospital)
    return hospital
