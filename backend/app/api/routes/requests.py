from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.database import get_db
from app.models.blood_request import BloodRequest
from app.schemas.blood_request import BloodRequestCreate, BloodRequestResponse, BloodRequestUpdate

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=BloodRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    payload: BloodRequestCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BloodRequest:
    req = BloodRequest(requester_user_id=current_user.id, **payload.model_dump())
    db.add(req)
    await db.flush()
    await db.refresh(req)
    return req


@router.get("", response_model=list[BloodRequestResponse])
async def list_requests(status_filter: str | None = None, db: AsyncSession = Depends(get_db)) -> list[BloodRequest]:
    stmt = select(BloodRequest)
    if status_filter:
        stmt = stmt.where(BloodRequest.status == status_filter)
    result = await db.execute(stmt.order_by(BloodRequest.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{request_id}", response_model=BloodRequestResponse)
async def get_request(request_id: str, db: AsyncSession = Depends(get_db)) -> BloodRequest:
    result = await db.execute(select(BloodRequest).where(BloodRequest.id == request_id))
    req = result.scalar_one_or_none()
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return req


@router.patch("/{request_id}", response_model=BloodRequestResponse)
async def update_request(
    request_id: str,
    payload: BloodRequestUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BloodRequest:
    result = await db.execute(select(BloodRequest).where(BloodRequest.id == request_id))
    req = result.scalar_one_or_none()
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(req, field, value)
    await db.flush()
    await db.refresh(req)
    return req
