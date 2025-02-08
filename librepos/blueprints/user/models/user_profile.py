import enum

from sqlalchemy import Enum

from librepos.extensions import db
from librepos.utils.sqlalchemy import CRUDMixin


class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    NOT_SPECIFIED = "NOT_SPECIFIED"


class UserProfile(CRUDMixin, db.Model):
    # ForeignKeys
    user_id = db.Column(
        db.String, db.ForeignKey("user.id"), nullable=False, unique=True
    )

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(Enum(Gender), nullable=False, default=Gender.NOT_SPECIFIED)
    phone_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255))

    email_verified = db.Column(db.Boolean, default=False)
    phone_number_verified = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship("User", back_populates="profile")

    # TODO 2/8/25 : move the following columns to a separate user_config_options table
    # language = db.Column(db.String(5), default="en")
    # timezone = db.Column(db.String(50))
    # dark_mode_enabled = db.Column(db.Boolean, default=False)

    @property
    def full_name(self) -> str:
        # Gather available name parts and return a space-separated full name.
        name_parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(part for part in name_parts if part)
