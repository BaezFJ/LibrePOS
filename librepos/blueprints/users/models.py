from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime


class User(db.Model, UserMixin):
    """User model."""

    __tablename__ = "users"

    def __init__(self, username: str, password: str, **kwargs):
        super(User, self).__init__(**kwargs)
        """Create instance."""
        self.username = username.lower()
        self.password = generate_password_hash(password)
        self.created_at = timezone_aware_datetime()

    # ForeignKeys
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)

    # Columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Relationships
    role = db.relationship("Role", back_populates="users")
    profile = db.relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def has_permission(self, permission_name: str) -> bool:
        if not self.role:
            return False

        return self.role.has_permission(permission_name)

    @property
    def email(self) -> str | None:
        return self.profile.email if self.profile else None


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
