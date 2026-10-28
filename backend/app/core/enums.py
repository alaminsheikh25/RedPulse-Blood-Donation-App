from __future__ import annotations

import enum


class UserRole(str, enum.Enum):
    DONOR = "donor"
    HOSPITAL_STAFF = "hospital_staff"
    BLOOD_BANK_STAFF = "blood_bank_staff"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class BloodGroup(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class RhFactor(str, enum.Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class DonationType(str, enum.Enum):
    WHOLE_BLOOD = "whole_blood"
    PLATELETS = "platelets"
    PLASMA = "plasma"
    DOUBLE_RED_CELLS = "double_red_cells"


class DonationStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DEFERRED = "deferred"
    NO_SHOW = "no_show"


class RequestUrgency(str, enum.Enum):
    ROUTINE = "routine"
    URGENT = "urgent"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class RequestStatus(str, enum.Enum):
    OPEN = "open"
    MATCHING = "matching"
    PARTIALLY_FULFILLED = "partially_fulfilled"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class NotificationChannel(str, enum.Enum):
    PUSH = "push"
    SMS = "sms"
    EMAIL = "email"
    IN_APP = "in_app"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    READ = "read"


class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InventoryStatus(str, enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    EXPIRED = "expired"
    DISCARDED = "discarded"


class MatchStatus(str, enum.Enum):
    PENDING = "pending"
    CONTACTED = "contacted"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    COMPLETED = "completed"
    EXPIRED = "expired"
