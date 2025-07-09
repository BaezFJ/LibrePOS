from datetime import datetime
from typing import List
from typing import TYPE_CHECKING, Optional

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from librepos.extensions import db
from librepos.utils import timezone_aware_datetime

if TYPE_CHECKING:
    from .role import Role
    from librepos.features.orders.models import ShopOrder


class User(UserMixin, db.Model):
    """User model."""

    __tablename__ = "users"

    def __init__(
            self,
            role_id: int,
            username: str,
            email: str,
            password: str,
            **kwargs,
    ):
        super(User, self).__init__(**kwargs)
        """Create instance."""
        self.role_id = role_id
        self.username = username.lower()
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.created_at = timezone_aware_datetime()

        self.set_default_image()

    # ForeignKeys
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime]

    # Authentication
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    failed_login_count: Mapped[int] = mapped_column(default=0)

    # Details
    first_name: Mapped[Optional[str]]
    middle_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    gender: Mapped[Optional[str]]
    marital_status: Mapped[Optional[str]]
    birthday: Mapped[Optional[datetime]]
    image: Mapped[Optional[str]]

    # ContactInfo
    email: Mapped[str] = mapped_column(unique=True, index=True)
    email_confirmed: Mapped[bool] = mapped_column(default=False)
    phone: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    phone_confirmed: Mapped[bool] = mapped_column(default=False)

    # AddressInfo
    address: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    state: Mapped[Optional[str]]
    zipcode: Mapped[Optional[str]]
    country: Mapped[Optional[str]]

    # ActivityTracking
    sign_in_count: Mapped[int] = mapped_column(default=0)
    current_sign_in_on: Mapped[Optional[datetime]]
    current_sign_in_ip: Mapped[Optional[str]]
    current_user_agent: Mapped[Optional[str]]
    last_sign_in_on: Mapped[Optional[datetime]]
    last_sign_in_ip: Mapped[Optional[str]]
    last_user_agent: Mapped[Optional[str]]
    last_password_change: Mapped[Optional[datetime]]

    # Relationships
    role: Mapped["Role"] = relationship(back_populates="users")
    orders: Mapped[List["ShopOrder"]] = relationship("ShopOrder", back_populates="user")

    # TODO (6/21/25): Move authentication, activity logging, and access control related functions to corresponding repositories
    # Functions to move:
    # - check_password(): Move to AuthenticationRepository
    # - record_sign_in(), handle_failed_login(), reset_failed_login_count(): Move to ActivityTrackingRepository
    # - has_permission(): Move to AccessControlRepository

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}"

    def has_permission(self, permission_name: str) -> bool:
        if not self.role:
            return False
        return self.role.has_permission(permission_name)

    def set_default_image(self):
        if self.gender == "male":
            self.image = "images/default_male_user.png"

        if self.gender == "female":
            self.image = "images/default_female_user.png"

    def record_sign_in(self, ip: str, agent: str):
        self.sign_in_count += 1
        self.current_sign_in_on = timezone_aware_datetime()
        self.current_sign_in_ip = ip
        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_user_agent = agent
        self.last_user_agent = agent

        db.session.commit()

    def handle_failed_login(self):
        self.failed_login_count += 1
        if self.failed_login_count >= 3:
            self.active = False
        db.session.commit()

    def reset_failed_login_count(self):
        self.failed_login_count = 0
        db.session.commit()
