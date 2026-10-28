from __future__ import annotations

from app.core.enums import BloodGroup

# Recipient can receive from donors of these groups.
COMPATIBILITY: dict[BloodGroup, set[BloodGroup]] = {
    BloodGroup.O_NEG: {BloodGroup.O_NEG},
    BloodGroup.O_POS: {BloodGroup.O_NEG, BloodGroup.O_POS},
    BloodGroup.A_NEG: {BloodGroup.O_NEG, BloodGroup.A_NEG},
    BloodGroup.A_POS: {BloodGroup.O_NEG, BloodGroup.O_POS, BloodGroup.A_NEG, BloodGroup.A_POS},
    BloodGroup.B_NEG: {BloodGroup.O_NEG, BloodGroup.B_NEG},
    BloodGroup.B_POS: {BloodGroup.O_NEG, BloodGroup.O_POS, BloodGroup.B_NEG, BloodGroup.B_POS},
    BloodGroup.AB_NEG: {BloodGroup.O_NEG, BloodGroup.A_NEG, BloodGroup.B_NEG, BloodGroup.AB_NEG},
    BloodGroup.AB_POS: {
        BloodGroup.O_NEG,
        BloodGroup.O_POS,
        BloodGroup.A_NEG,
        BloodGroup.A_POS,
        BloodGroup.B_NEG,
        BloodGroup.B_POS,
        BloodGroup.AB_NEG,
        BloodGroup.AB_POS,
    },
}

# Donor can donate to these recipient groups.
DONOR_TO_RECIPIENT: dict[BloodGroup, set[BloodGroup]] = {}
for recipient, donors in COMPATIBILITY.items():
    for donor in donors:
        DONOR_TO_RECIPIENT.setdefault(donor, set()).add(recipient)


def can_donate_to(donor: BloodGroup, recipient: BloodGroup) -> bool:
    return donor in COMPATIBILITY.get(recipient, set())


def compatible_donors_for(recipient: BloodGroup) -> set[BloodGroup]:
    return set(COMPATIBILITY.get(recipient, set()))


def compatible_recipients_for(donor: BloodGroup) -> set[BloodGroup]:
    return set(DONOR_TO_RECIPIENT.get(donor, set()))


def is_universal_donor(group: BloodGroup) -> bool:
    return group == BloodGroup.O_NEG


def is_universal_recipient(group: BloodGroup) -> bool:
    return group == BloodGroup.AB_POS
