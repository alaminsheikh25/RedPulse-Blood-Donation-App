from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.blood_request import BloodRequest
from app.models.match import Match
from app.services.matching import find_candidates

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("/request/{request_id}/run")
async def run_matching(request_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BloodRequest).where(BloodRequest.id == request_id))
    req = result.scalar_one_or_none()
    if req is None:
        raise HTTPException(status_code=404, detail="Request not found")
    candidates = await find_candidates(db, req.blood_group, req.urgency, req.latitude, req.longitude)
    created = 0
    for c in candidates:
        match = Match(request_id=req.id, donor_id=c.donor.id, score=c.score, distance_km=c.distance_km)
        db.add(match)
        created += 1
    req.status = req.status.MATCHING if hasattr(req.status, "MATCHING") else req.status
    await db.flush()
    return {"request_id": request_id, "candidates": len(candidates), "created": created}


@router.get("/request/{request_id}")
async def list_matches(request_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Match).where(Match.request_id == request_id).order_by(Match.score.desc()))
    return [{"id": m.id, "donor_id": m.donor_id, "score": m.score, "distance_km": m.distance_km, "status": m.status.value} for m in result.scalars().all()]
