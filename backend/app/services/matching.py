from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.enums import BloodGroup, RequestUrgency
from app.models.donor import Donor
from app.services.blood_compatibility import compatible_donors_for
from app.services.eligibility import evaluate_donor_eligibility
from app.utils.geo import haversine_km


@dataclass
class MatchCandidate:
    donor: Donor
    distance_km: Optional[float]
    score: float
    reasons: list[str]


def _urgency_weight(urgency: RequestUrgency) -> float:
    return {
        RequestUrgency.ROUTINE: 1.0,
        RequestUrgency.URGENT: 1.3,
        RequestUrgency.CRITICAL: 1.6,
        RequestUrgency.EMERGENCY: 2.0,
    }.get(urgency, 1.0)


def score_donor(donor: Donor, request_blood_group: BloodGroup, request_lat: Optional[float], request_lon: Optional[float], urgency: RequestUrgency) -> tuple[float, Optional[float], list[str]]:
    reasons: list[str] = []
    distance: Optional[float] = None
    score = 0.0

    if request_lat is not None and request_lon is not None and donor.latitude is not None and donor.longitude is not None:
        distance = haversine_km(request_lat, request_lon, donor.latitude, donor.longitude)
        if distance <= settings.default_search_radius_km:
            score += max(0.0, 40.0 - (distance / settings.default_search_radius_km) * 40.0)
            reasons.append(f"within {distance:.1f}km")
        else:
            score += max(0.0, 10.0 - (distance / settings.max_search_radius_km) * 10.0)
    else:
        score += 5.0

    score += donor.reliability_score * 20.0
    score += donor.response_rate * 15.0
    score += min(donor.total_donations, 20) * 0.5

    if donor.last_donation_date is not None:
        days_since = (date.today() - donor.last_donation_date).days
        score += min(days_since / 10.0, 10.0)

    score *= _urgency_weight(urgency)
    return score, distance, reasons


async def find_candidates(
    db: AsyncSession,
    request_blood_group: BloodGroup,
    urgency: RequestUrgency,
    latitude: Optional[float],
    longitude: Optional[float],
    radius_km: Optional[float] = None,
    limit: int = 50,
) -> list[MatchCandidate]:
    radius = radius_km or settings.max_search_radius_km
    compatible = compatible_donors_for(request_blood_group)

    stmt = select(Donor).where(Donor.blood_group.in_(compatible), Donor.is_available.is_(True))
    result = await db.execute(stmt)
    donors = result.scalars().all()

    candidates: list[MatchCandidate] = []
    for donor in donors:
        elig = evaluate_donor_eligibility(donor)
        if not elig.eligible:
            continue
        if latitude is not None and longitude is not None and donor.latitude is not None and donor.longitude is not None:
            dist = haversine_km(latitude, longitude, donor.latitude, donor.longitude)
            if dist > radius:
                continue
        score, distance, reasons = score_donor(donor, request_blood_group, latitude, longitude, urgency)
        candidates.append(MatchCandidate(donor=donor, distance_km=distance, score=score, reasons=reasons))

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:limit]
