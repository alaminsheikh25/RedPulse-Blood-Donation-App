import pytest

from app.core.enums import BloodGroup
from app.services.blood_compatibility import can_donate_to, compatible_donors_for, is_universal_donor, is_universal_recipient


def test_o_neg_universal_donor():
    assert is_universal_donor(BloodGroup.O_NEG)
    for recipient in BloodGroup:
        assert can_donate_to(BloodGroup.O_NEG, recipient)


def test_ab_pos_universal_recipient():
    assert is_universal_recipient(BloodGroup.AB_POS)
    for donor in BloodGroup:
        assert can_donate_to(donor, BloodGroup.AB_POS)


def test_compatibility_matrix_symmetry():
    for recipient in BloodGroup:
        donors = compatible_donors_for(recipient)
        for d in donors:
            assert can_donate_to(d, recipient)


def test_a_pos_cannot_receive_b():
    assert not can_donate_to(BloodGroup.B_POS, BloodGroup.A_POS)
    assert not can_donate_to(BloodGroup.B_NEG, BloodGroup.A_POS)
