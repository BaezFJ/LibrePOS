from enum import StrEnum


class OrderStateEnum(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    VOIDED = "voided"
