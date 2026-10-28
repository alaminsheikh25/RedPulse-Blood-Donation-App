from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.campaign import Campaign

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_campaign(payload: dict, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    campaign = Campaign(organizer_user_id=current_user.id, **{k: v for k, v in payload.items() if k in {"title", "description", "location", "latitude", "longitude", "start_date", "end_date", "target_blood_groups", "target_units", "is_public", "hospital_id"}})
    db.add(campaign)
    await db.flush()
    await db.refresh(campaign)
    return {"id": campaign.id, "title": campaign.title}


@router.get("")
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campaign).order_by(Campaign.start_date.desc()))
    return [{"id": c.id, "title": c.title, "status": c.status.value, "start_date": c.start_date, "end_date": c.end_date} for c in result.scalars().all()]
