from datetime import date, timedelta

from app.core.enums import DonationType, Gender
from app.models.donor import Donor
from app.services.eligibility import evaluate_donor_eligibility


def _make_donor(**overrides):
    base = dict(
        user_id="u1",
        blood_group=__import__("app.core.enums", fromlist=["BloodGroup"]).BloodGroup.O_POS,
        date_of_birth=date(1990, 1, 1),
        gender=Gender.MALE,
        weight_kg=70.0,
        hemoglobin_g_dl=14.0,
        is_available=True,
        total_donations=0,
    )
    base.update(overrides)
    return Donor(**base)


def test_eligible_donor():
    donor = _make_donor()
    res = evaluate_donor_eligibility(donor)
    assert res.eligible
    assert res.reasons == []


def test_underweight():
    donor = _make_donor(weight_kg=40.0)
    res = evaluate_donor_eligibility(donor)
    assert not res.eligible
    assert any("Weight" in r for r in res.reasons)


def test_recent_donation_deferral():
    donor = _make_donor(last_donation_date=date.today() - timedelta(days=10))
    res = evaluate_donor_eligibility(donor)
    assert not res.eligible
    assert any("Last donation" in r for r in res.reasons)


def test_chronic_illness():
    donor = _make_donor(has_chronic_illness=True)
    res = evaluate_donor_eligibility(donor)
    assert not res.eligible
