from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from app.config import settings
from app.core.enums import DonationType, Gender
from app.models.donor import Donor


class EligibilityResult:
    def __init__(self, eligible: bool, reasons: list[str]):
        self.eligible = eligible
        self.reasons = reasons

    def to_dict(self) -> dict:
        return {"eligible": self.eligible, "reasons": self.reasons}


def evaluate_donor_eligibility(donor: Donor, donation_type: DonationType = DonationType.WHOLE_BLOOD, as_of: Optional[date] = None) -> EligibilityResult:
    as_of = as_of or date.today()
    reasons: list[str] = []

    age = donor.age(as_of)
    if age < settings.min_donor_age:
        reasons.append(f"Age {age} is below minimum {settings.min_donor_age}")
    if age > settings.max_donor_age:
        reasons.append(f"Age {age} exceeds maximum {settings.max_donor_age}")

    if donor.weight_kg < settings.min_donor_weight_kg:
        reasons.append(f"Weight {donor.weight_kg}kg below minimum {settings.min_donor_weight_kg}kg")

    if donor.hemoglobin_g_dl is None or donor.hemoglobin_g_dl < settings.min_hemoglobin_g_dl:
        reasons.append(f"Hemoglobin {donor.hemoglobin_g_dl} below minimum {settings.min_hemoglobin_g_dl} g/dL")

    if donor.has_chronic_illness:
        reasons.append("Chronic illness disqualifies donation")
    if donor.on_medication:
        reasons.append("Current medication may disqualify donation")
    if donor.recent_tattoo_piercing:
        reasons.append("Recent tattoo/piercing within deferral window")
    if donor.recent_travel_risk:
        reasons.append("Recent travel to risk area")

    if donor.deferred_until is not None and donor.deferred_until > as_of:
        reasons.append(f"Deferred until {donor.deferred_until}")

    if donor.last_donation_date is not None:
        interval = (as_of - donor.last_donation_date).days
        required = _required_interval(donation_type)
        if interval < required:
            reasons.append(f"Last donation {interval} days ago; required interval {required} days")

    if not donor.is_available:
        reasons.append("Donor marked unavailable")

    return EligibilityResult(eligible=len(reasons) == 0, reasons=reasons)


def _required_interval(donation_type: DonationType) -> int:
    if donation_type == DonationType.PLATELETS:
        return settings.platelet_interval_days
    if donation_type == DonationType.PLASMA:
        return settings.plasma_interval_days
    return settings.min_donation_interval_days


def next_eligible_date(donor: Donor, donation_type: DonationType = DonationType.WHOLE_BLOOD) -> Optional[date]:
    if donor.last_donation_date is None:
        return date.today()
    return donor.last_donation_date + timedelta(days=_required_interval(donation_type))
