from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.blood_request import BloodRequest
from app.models.donation import Donation
from app.models.donor import Donor
from app.models.inventory import Inventory

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary")
async def summary(db: AsyncSession = Depends(get_db)):
    donors = (await db.execute(select(func.count()).select_from(Donor))).scalar_one()
    requests = (await db.execute(select(func.count()).select_from(BloodRequest))).scalar_one()
    donations = (await db.execute(select(func.count()).select_from(Donation))).scalar_one()
    units = (await db.execute(select(func.coalesce(func.sum(Inventory.units_available), 0)))).scalar_one()
    return {
        "total_donors": donors,
        "total_requests": requests,
        "total_donations": donations,
        "units_available": units,
    }
