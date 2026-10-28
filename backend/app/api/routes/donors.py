from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.donor import Donor
from app.models.user import User
from app.schemas.donor import DonorCreate, DonorResponse, DonorUpdate, EligibilityResponse
from app.services.eligibility import evaluate_donor_eligibility, next_eligible_date

router = APIRouter(prefix="/donors", tags=["donors"])


@router.post("", response_model=DonorResponse, status_code=status.HTTP_201_CREATED)
async def create_donor_profile(
    payload: DonorCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Donor:
    existing = await db.execute(select(Donor).where(Donor.user_id == current_user.id))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Donor profile already exists")
    donor = Donor(user_id=current_user.id, **payload.model_dump())
    db.add(donor)
    await db.flush()
    await db.refresh(donor)
    return donor


@router.get("/me", response_model=DonorResponse)
async def my_donor_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Donor:
    result = await db.execute(select(Donor).where(Donor.user_id == current_user.id))
    donor = result.scalar_one_or_none()
    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donor profile not found")
    return donor


@router.patch("/me", response_model=DonorResponse)
async def update_my_donor_profile(
    payload: DonorUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Donor:
    result = await db.execute(select(Donor).where(Donor.user_id == current_user.id))
    donor = result.scalar_one_or_none()
    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donor profile not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(donor, field, value)
    await db.flush()
    await db.refresh(donor)
    return donor


@router.get("/me/eligibility", response_model=EligibilityResponse)
async def my_eligibility(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> EligibilityResponse:
    result = await db.execute(select(Donor).where(Donor.user_id == current_user.id))
    donor = result.scalar_one_or_none()
    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donor profile not found")
    elig = evaluate_donor_eligibility(donor)
    ned = next_eligible_date(donor) if not elig.eligible else None
    return EligibilityResponse(eligible=elig.eligible, reasons=elig.reasons, next_eligible_date=ned)


@router.get("/{donor_id}", response_model=DonorResponse)
async def get_donor(donor_id: str, db: AsyncSession = Depends(get_db)) -> Donor:
    result = await db.execute(select(Donor).where(Donor.id == donor_id))
    donor = result.scalar_one_or_none()
    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donor not found")
    return donor
