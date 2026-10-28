from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryResponse, InventoryUpdate

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    payload: InventoryCreate,
    current_user=Depends(require_roles("admin", "super_admin", "blood_bank_staff", "hospital_staff")),
    db: AsyncSession = Depends(get_db),
) -> Inventory:
    item = Inventory(**payload.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("", response_model=list[InventoryResponse])
async def list_inventory(hospital_id: str | None = None, db: AsyncSession = Depends(get_db)) -> list[Inventory]:
    stmt = select(Inventory)
    if hospital_id:
        stmt = stmt.where(Inventory.hospital_id == hospital_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.patch("/{item_id}", response_model=InventoryResponse)
async def update_inventory(
    item_id: str,
    payload: InventoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> Inventory:
    result = await db.execute(select(Inventory).where(Inventory.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.flush()
    await db.refresh(item)
    return item
