from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.donation import Donation
from app.models.donor import Donor
from app.schemas.donation import DonationCreate, DonationResponse, DonationUpdate

router = APIRouter(prefix="/donations", tags=["donations"])


@router.post("", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(
    payload: DonationCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Donation:
    result = await db.execute(select(Donor).where(Donor.user_id == current_user.id))
    donor = result.scalar_one_or_none()
    if donor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donor profile required")
    donation = Donation(donor_id=donor.id, **payload.model_dump())
    db.add(donation)
    await db.flush()
    await db.refresh(donation)
    return donation


@router.get("", response_model=list[DonationResponse])
async def list_donations(db: AsyncSession = Depends(get_db)) -> list[Donation]:
    result = await db.execute(select(Donation).order_by(Donation.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{donation_id}", response_model=DonationResponse)
async def get_donation(donation_id: str, db: AsyncSession = Depends(get_db)) -> Donation:
    result = await db.execute(select(Donation).where(Donation.id == donation_id))
    donation = result.scalar_one_or_none()
    if donation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    return donation


@router.patch("/{donation_id}", response_model=DonationResponse)
async def update_donation(
    donation_id: str,
    payload: DonationUpdate,
    db: AsyncSession = Depends(get_db),
) -> Donation:
    result = await db.execute(select(Donation).where(Donation.id == donation_id))
    donation = result.scalar_one_or_none()
    if donation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(donation, field, value)
    await db.flush()
    await db.refresh(donation)
    return donation
