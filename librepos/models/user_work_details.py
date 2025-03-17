import enum

from sqlalchemy import Enum

from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class CompensationType(enum.Enum):
    FIXED = "FIXED"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    BIMONTHLY = "BIMONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"


class UserWorkDetails(CRUDMixin, db.Model):
    # ForeignKeys
    user_id = db.Column(
        db.String, db.ForeignKey("user.id"), nullable=False, unique=True
    )

    # Columns
    id = db.Column(db.Integer, primary_key=True, index=True)
    hire_date = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    start_compensation = db.Column(db.Integer, nullable=False)
    start_compensation_type = db.Column(
        Enum(CompensationType), nullable=False, default=CompensationType.HOURLY
    )
    current_compensation = db.Column(db.Integer, nullable=False)
    current_compensation_type = db.Column(
        Enum(CompensationType), nullable=False, default=CompensationType.HOURLY
    )
    end_compensation = db.Column(db.Integer, nullable=True)
    end_compensation_type = db.Column(
        Enum(CompensationType), nullable=True, default=CompensationType.HOURLY
    )

    # TODO 2/6/25 : add the assigned_terminal_id, assigned_devices, store_id

    # Relationships
    user = db.relationship("User", back_populates="work_details")

    def __init__(self, user_id, hire_date, start_date, start_compensation, **kwargs):
        self.user_id = user_id
        super(UserWorkDetails, self).__init__(**kwargs)
        self.hire_date = hire_date
        self.start_date = start_date
        self.start_compensation = start_compensation
        self.current_compensation = start_compensation
