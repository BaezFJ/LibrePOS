import enum

from sqlalchemy import Enum

from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class ShiftStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    ON_VACATION = "ON_VACATION"
    ON_BREAK = "ON_BREAK"
    OFF_WORK = "OFF_WORK"


class UserShiftDetails(CRUDMixin, db.Model):
    # ForeignKeys
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    # Columns
    id = db.Column(db.Integer, primary_key=True, index=True)
    date = db.Column(db.Date, nullable=False)
    shift_status = db.Column(
        Enum(ShiftStatus), nullable=False, default=ShiftStatus.ACTIVE
    )
    shift_start_time = db.Column(db.DateTime)
    shift_end_time = db.Column(db.DateTime)

    # Relationships
    user = db.relationship("User", back_populates="shift_details")
