from librepos.extensions import db
from librepos.utils import timezone_aware_datetime


class UserProfile(db.Model):
    """UserProfile model."""

    __tablename__ = "user_profile"

    def __init__(self, user_id: int, **kwargs):
        super(UserProfile, self).__init__(**kwargs)
        self.user_id = user_id

    # ForeignKeys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    # Columns
    first_name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    marital_status = db.Column(db.String(10), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    # ContactInfo
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=timezone_aware_datetime)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=timezone_aware_datetime,
        onupdate=timezone_aware_datetime,
    )

    # Relationships
    user = db.relationship("User", back_populates="profile")
