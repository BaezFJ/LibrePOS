from enum import StrEnum


class OrderStateEnum(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    VOIDED = "voided"


class DateFormatEnum(StrEnum):
    DDMMYYYY = "%d/%m/%Y"
    MMDDYYYY = "%m/%d/%Y"
    DDMMYY = "%d/%m/%y"
    MMDDYY = "%m/%d/%y"
    YYYMMDD = "%Y/%m/%d"
